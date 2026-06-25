from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UniversityViewSet

router = DefaultRouter()
router.register(r"universities", UniversityViewSet, basename="university")

urlpatterns = [
    path("", include(router.urls)),
]
