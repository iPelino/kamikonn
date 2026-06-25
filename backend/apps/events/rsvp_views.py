import uuid
from datetime import UTC, datetime

from django.db import transaction
from django.http import HttpResponse
from icalendar import Calendar
from icalendar import Event as CalEvent
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.events.models import RSVP, Event, RSVPStatus, SavedEvent
from apps.events.rsvp_serializers import RSVPSerializer, SavedEventSerializer


class RSVPViewSet(viewsets.GenericViewSet):
    """
    Handles RSVP creation, cancellation, and .ics calendar export for events.

    POST   /events/{event_slug}/rsvp/          -- create or re-activate an RSVP
    DELETE /events/{event_slug}/rsvp/          -- cancel RSVP (promotes waitlisted user)
    GET    /events/{event_slug}/rsvp/calendar/ -- download .ics file
    """

    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_event(self, slug: str) -> Event:
        return Event.objects.get(slug=slug)

    @action(detail=False, methods=["post", "delete"], url_path="rsvp")
    def rsvp(self, request, event_slug: str | None = None):
        """Dispatch POST (create) and DELETE (cancel) on the same URL."""
        if request.method == "POST":
            return self._create_rsvp(request, event_slug)
        return self._cancel_rsvp(request, event_slug)

    def _create_rsvp(self, request, event_slug: str | None):
        """RSVP to an event. Auto-assigns ATTENDING or WAITLISTED based on capacity."""
        try:
            event = self._get_event(event_slug)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            # Lock the event row to prevent concurrent capacity over-booking.
            locked_event = Event.objects.select_for_update().get(pk=event.pk)

            # Reject duplicate RSVPs (non-cancelled).
            existing = (
                RSVP.objects.filter(event=locked_event, user=request.user)
                .exclude(status=RSVPStatus.CANCELLED)
                .first()
            )
            if existing:
                serializer = self.get_serializer(existing)
                return Response(
                    {"detail": "Already RSVPed to this event.", "rsvp": serializer.data},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Determine slot availability.
            if locked_event.capacity == 0:
                rsvp_status = RSVPStatus.ATTENDING
            else:
                attending_count = RSVP.objects.filter(
                    event=locked_event, status=RSVPStatus.ATTENDING
                ).count()
                rsvp_status = (
                    RSVPStatus.ATTENDING
                    if attending_count < locked_event.capacity
                    else RSVPStatus.WAITLISTED
                )

            # Re-use a previously cancelled RSVP record if it exists.
            rsvp, _ = RSVP.objects.update_or_create(
                event=locked_event,
                user=request.user,
                defaults={"status": rsvp_status},
            )

        serializer = self.get_serializer(rsvp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _cancel_rsvp(self, request, event_slug: str | None):
        """Cancel an RSVP, and promote the first waitlisted user to ATTENDING."""
        try:
            event = self._get_event(event_slug)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            locked_event = Event.objects.select_for_update().get(pk=event.pk)

            try:
                rsvp = RSVP.objects.select_for_update().get(
                    event=locked_event,
                    user=request.user,
                )
            except RSVP.DoesNotExist:
                return Response(
                    {"detail": "No active RSVP found for this event."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if rsvp.status == RSVPStatus.CANCELLED:
                return Response(
                    {"detail": "RSVP is already cancelled."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            was_attending = rsvp.status == RSVPStatus.ATTENDING
            rsvp.status = RSVPStatus.CANCELLED
            rsvp.save(update_fields=["status", "updated_at"])

            # Promote the oldest waitlisted user if a capacity slot just freed up.
            if was_attending and locked_event.capacity != 0:
                next_in_line = (
                    RSVP.objects.select_for_update()
                    .filter(event=locked_event, status=RSVPStatus.WAITLISTED)
                    .order_by("created_at")
                    .first()
                )
                if next_in_line:
                    next_in_line.status = RSVPStatus.ATTENDING
                    next_in_line.save(update_fields=["status", "updated_at"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="rsvp/calendar")
    def calendar(self, request, event_slug: str | None = None):
        """Return an .ics calendar file for the event."""
        try:
            event = self._get_event(event_slug)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        cal = Calendar()
        cal.add("prodid", "-//KamiKonn//kamconnect.rw//EN")
        cal.add("version", "2.0")

        cal_event = CalEvent()
        cal_event.add("uid", str(uuid.uuid4()))
        cal_event.add("summary", event.title)
        cal_event.add("description", event.description or "")
        cal_event.add("location", event.location or "")

        if event.start_time:
            cal_event.add("dtstart", event.start_time)
        if event.end_time:
            cal_event.add("dtend", event.end_time)

        now = datetime.now(tz=UTC)
        cal_event.add("dtstamp", now)

        cal.add_component(cal_event)

        filename = f"{event.slug}.ics"
        response = HttpResponse(
            cal.to_ical(),
            content_type="text/calendar; charset=utf-8",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class SavedEventViewSet(viewsets.GenericViewSet):
    """
    POST   /events/{event_slug}/save/   -- save an event
    DELETE /events/{event_slug}/save/   -- unsave an event
    """

    serializer_class = SavedEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_event(self, slug: str) -> Event:
        return Event.objects.get(slug=slug)

    @action(detail=False, methods=["post", "delete"], url_path="save")
    def save_event(self, request, event_slug: str | None = None):
        """Dispatch POST (save) and DELETE (unsave) on the same URL."""
        if request.method == "POST":
            return self._save_event(request, event_slug)
        return self._unsave_event(request, event_slug)

    def _save_event(self, request, event_slug: str | None):
        """Bookmark an event for the current user."""
        try:
            event = self._get_event(event_slug)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        saved, created = SavedEvent.objects.get_or_create(event=event, user=request.user)
        if not created:
            serializer = self.get_serializer(saved)
            return Response(
                {"detail": "Event already saved.", "saved": serializer.data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(saved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _unsave_event(self, request, event_slug: str | None):
        """Remove a saved event bookmark for the current user."""
        try:
            event = self._get_event(event_slug)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = SavedEvent.objects.filter(event=event, user=request.user).delete()
        if not deleted:
            return Response(
                {"detail": "Event was not saved."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
