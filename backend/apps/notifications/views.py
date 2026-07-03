from rest_framework import generics, permissions

from .models import NotificationPreference
from .serializers import NotificationPreferenceSerializer


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's notification preferences."""

    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return obj
