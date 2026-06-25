from rest_framework import permissions


class IsUniversityModerator(permissions.BasePermission):
    """
    Allows access only to users who are moderators of at least one university.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.moderated_universities.exists()
        )
