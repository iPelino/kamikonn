from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrganizerProfile
from .serializers import BecomeOrganizerSerializer, OrganizerProfileSerializer


class BecomeOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, "organizer_profile"):
            return Response(
                {"detail": "User is already an organizer."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BecomeOrganizerSerializer(data=request.data)
        if serializer.is_valid():
            profile = OrganizerProfile.objects.create(
                user=user,
                bio=serializer.validated_data.get("bio", ""),
                website=serializer.validated_data.get("website", ""),
                social_links=serializer.validated_data.get("social_links", {}),
            )
            return Response(
                OrganizerProfileSerializer(profile).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerProfileDetailView(generics.RetrieveAPIView):
    queryset = OrganizerProfile.objects.all()
    serializer_class = OrganizerProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = "user__username"  # Wait, username is not required. Let's use user__id or pk.

    def get_object(self):
        # We can look up by user id
        user_id = self.kwargs.get("user_id")
        try:
            return OrganizerProfile.objects.get(user__id=user_id)
        except OrganizerProfile.DoesNotExist as e:
            from django.http import Http404

            raise Http404("Organizer not found.") from e


class CurrentOrganizerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.organizer_profile
        except OrganizerProfile.DoesNotExist as e:
            from django.http import Http404

            raise Http404("You are not an organizer.") from e
