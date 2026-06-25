from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.moderation.models import (
    FlagReport,
    FlagStatus,
    ModerationAction,
    ModerationLog,
)
from apps.moderation.serializers import FlagReportSerializer, ModerationLogSerializer
from apps.universities.permissions import IsUniversityModerator


class FlagReportViewSet(viewsets.ModelViewSet):
    """
    Users can flag events (create).
    Moderators can view flags and resolve/dismiss them.
    """

    queryset = FlagReport.objects.select_related("event", "reporter")
    serializer_class = FlagReportSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsUniversityModerator()]

    def perform_create(self, serializer):
        report = serializer.save(reporter=self.request.user)
        # Log the flag
        ModerationLog.objects.create(
            event=report.event,
            moderator=self.request.user,
            action=ModerationAction.FLAGGED,
            reason=report.reason,
        )

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        report = self.get_object()
        report.status = FlagStatus.RESOLVED
        report.save()

        ModerationLog.objects.create(
            event=report.event,
            moderator=request.user,
            action=ModerationAction.FLAG_RESOLVED,
            reason="Resolved flag",
        )
        return Response({"status": "resolved"})

    @action(detail=True, methods=["post"])
    def dismiss(self, request, pk=None):
        report = self.get_object()
        report.status = FlagStatus.DISMISSED
        report.save()

        ModerationLog.objects.create(
            event=report.event,
            moderator=request.user,
            action=ModerationAction.FLAG_DISMISSED,
            reason="Dismissed flag",
        )
        return Response({"status": "dismissed"})


class ModerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for the moderation log.
    Accessible by University Moderators.
    """

    queryset = ModerationLog.objects.select_related("event", "moderator")
    serializer_class = ModerationLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsUniversityModerator]
