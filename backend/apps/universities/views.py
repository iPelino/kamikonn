from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import University
from .serializers import UniversitySerializer

User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UniversityViewSet(viewsets.ModelViewSet):
    """
    CRUD for Universities. Admin only for C/U/D.
    """

    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign_moderator(self, request, pk=None):
        university = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        university.moderators.add(user)

        # Ensure user is in the 'University Moderator' group
        group, _ = Group.objects.get_or_create(name="University Moderator")
        user.groups.add(group)

        return Response({"status": "moderator assigned"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def remove_moderator(self, request, pk=None):
        university = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        university.moderators.remove(user)

        # If user is no longer a moderator of any university, remove them from the group
        if not user.moderated_universities.exists():
            group = Group.objects.filter(name="University Moderator").first()
            if group:
                user.groups.remove(group)

        return Response({"status": "moderator removed"}, status=status.HTTP_200_OK)
