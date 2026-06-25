from django.contrib.postgres.search import SearchQuery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from apps.events.filters import EventFilter
from apps.events.models import Category, Event
from apps.events.serializers import CategorySerializer, EventSerializer


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
