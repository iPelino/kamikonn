import csv
import io

from django.contrib.postgres.search import SearchQuery
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.events.filters import EventFilter
from apps.events.models import Category, Event, EventStatus
from apps.events.serializers import CategorySerializer, EventSerializer
from apps.universities.permissions import IsUniversityModerator


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for event categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class EventViewSet(viewsets.ModelViewSet):
    """
    Basic CRUD operations for events.
    Anyone can view APPROVED events.
    Only authenticated users can create drafts.
    """

    queryset = Event.objects.select_related("organizer", "category").prefetch_related(
        "universities"
    )
    serializer_class = EventSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = EventFilter
    ordering_fields = ["start_time", "created_at"]
    ordering = ["start_time"]
    search_fields = ["title", "description", "location"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()

        # If the user is unauthenticated, they only see APPROVED events
        if not self.request.user.is_authenticated:
            qs = qs.filter(status="APPROVED")
        else:
            pass

        # Postgres Full Text Search if 'q' is provided
        q = self.request.query_params.get("q")
        if q:
            query = SearchQuery(q)
            # First layer: Full text search using pre-computed GIN-indexed search_vector
            fts_qs = qs.filter(search_vector=query)

            if fts_qs.exists():
                qs = fts_qs
            else:
                # Second layer: Trigram similarity on title (with GIN pg_trgm index)
                from django.contrib.postgres.search import TrigramSimilarity

                qs = (
                    qs.annotate(similarity=TrigramSimilarity("title", q))
                    .filter(similarity__gt=0.1)
                    .order_by("-similarity", "-start_time")
                )

        return qs

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, slug=None):
        event = self.get_object()

        if event.status != EventStatus.DRAFT:
            return Response({"error": "Only events in DRAFT status can be submitted."}, status=400)

        # Validate required fields before allowing submission
        required_fields = ["start_time", "end_time", "location", "description"]
        missing = [field for field in required_fields if not getattr(event, field)]

        if missing:
            return Response({"error": f"Missing required fields: {', '.join(missing)}"}, status=400)

        # Auto-trust check: skip PENDING if organizer has 3+ clean (approved) events
        clean_events_count = Event.objects.filter(
            organizer=request.user, status=EventStatus.APPROVED
        ).count()
        if clean_events_count >= 3:
            event.status = EventStatus.APPROVED
            event.save()
            return Response({"status": "approved_auto", "event": event.slug})

        event.status = EventStatus.PENDING
        event.save()
        return Response({"status": "submitted", "event": event.slug})

    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser])
    def import_csv(self, request):
        if "file" not in request.FILES:
            return Response({"error": "No file provided"}, status=400)

        file = request.FILES["file"]
        if not file.name.endswith(".csv"):
            return Response({"error": "File must be a CSV"}, status=400)

        try:
            decoded_file = file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            events_created = 0
            errors = []

            for row_idx, row in enumerate(reader, start=1):
                title = row.get("title", "").strip()
                if not title:
                    errors.append(f"Row {row_idx}: Missing title")
                    continue

                start_time_str = row.get("start_time", "").strip()
                end_time_str = row.get("end_time", "").strip()
                start_time = parse_datetime(start_time_str) if start_time_str else None
                end_time = parse_datetime(end_time_str) if end_time_str else None

                description = row.get("description", "").strip()
                location = row.get("location", "").strip()
                is_virtual = str(row.get("is_virtual", "")).lower() in ["true", "1", "yes"]
                capacity_str = row.get("capacity", "0").strip()
                price_str = row.get("price", "0.00").strip()

                try:
                    capacity = int(capacity_str) if capacity_str else 0
                except ValueError:
                    capacity = 0

                try:
                    price = float(price_str) if price_str else 0.00
                except ValueError:
                    price = 0.00

                Event.objects.create(
                    title=title,
                    description=description,
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                    is_virtual=is_virtual,
                    capacity=capacity,
                    price=price,
                    organizer=request.user,
                    status=EventStatus.DRAFT,
                )
                events_created += 1

            return Response(
                {
                    "message": f"Successfully imported {events_created} events.",
                    "events_created": events_created,
                    "errors": errors,
                }
            )

        except Exception as e:
            return Response({"error": f"Error processing CSV: {str(e)}"}, status=400)


class ModerationEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for University Moderators to review pending events.
    """

    serializer_class = EventSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated, IsUniversityModerator]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Return pending events that belong to a university the current user moderates
        return (
            Event.objects.filter(
                status=EventStatus.PENDING,
                universities__moderators=self.request.user,
            )
            .select_related("organizer", "category")
            .prefetch_related("universities")
            .distinct()
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, slug=None):
        event = self.get_object()
        event.status = EventStatus.APPROVED
        event.save()

        from apps.moderation.models import ModerationAction, ModerationLog

        ModerationLog.objects.create(
            event=event,
            moderator=request.user,
            action=ModerationAction.APPROVED,
        )

        send_mail(
            subject=f"Your event '{event.title}' has been approved!",
            message=(
                f"Good news! Your event '{event.title}' "
                "has been approved by a university moderator and is now live."
            ),
            from_email="noreply@kamconnect.rw",
            recipient_list=[event.organizer.email],
            fail_silently=True,
        )

        return Response({"status": "approved", "event": event.slug})

    @action(detail=True, methods=["post"])
    def reject(self, request, slug=None):
        event = self.get_object()
        event.status = EventStatus.REJECTED
        event.save()

        from apps.moderation.models import ModerationAction, ModerationLog

        ModerationLog.objects.create(
            event=event,
            moderator=request.user,
            action=ModerationAction.REJECTED,
        )

        send_mail(
            subject=f"Your event '{event.title}' has been rejected",
            message=(
                f"Unfortunately, your event '{event.title}' "
                "has been rejected by a university moderator."
            ),
            from_email="noreply@kamconnect.rw",
            recipient_list=[event.organizer.email],
            fail_silently=True,
        )

        return Response({"status": "rejected", "event": event.slug})
