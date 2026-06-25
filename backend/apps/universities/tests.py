import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status

from apps.universities.models import University

pytestmark = pytest.mark.django_db


def test_list_universities(api_client):
    University.objects.create(name="ALU", short_name="ALU", domain="alueducation.com")
    url = reverse("university-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data.get("results", response.data)) == 1


def test_create_university_unauthorized(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    url = reverse("university-list")
    response = api_client.post(url, {"name": "Test Univ", "short_name": "TU", "domain": "tu.edu"})
    # Non-staff should not be able to create
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_university_admin(api_client, user_factory):
    admin = user_factory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)

    url = reverse("university-list")
    response = api_client.post(url, {"name": "Test Univ", "short_name": "TU", "domain": "tu.edu"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Test Univ"


def test_assign_moderator(api_client, user_factory):
    admin = user_factory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)

    univ = University.objects.create(name="ALU", short_name="ALU", domain="alueducation.com")
    user = user_factory()

    url = reverse("university-assign-moderator", args=[univ.id])
    response = api_client.post(url, {"user_id": user.id})
    assert response.status_code == status.HTTP_200_OK

    univ.refresh_from_db()
    assert user in univ.moderators.all()
    assert user.groups.filter(name="University Moderator").exists()


def test_remove_moderator(api_client, user_factory):
    admin = user_factory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)

    univ = University.objects.create(name="ALU", short_name="ALU", domain="alueducation.com")
    user = user_factory()

    group, _ = Group.objects.get_or_create(name="University Moderator")
    user.groups.add(group)
    univ.moderators.add(user)

    url = reverse("university-remove-moderator", args=[univ.id])
    response = api_client.post(url, {"user_id": user.id})
    assert response.status_code == status.HTTP_200_OK

    univ.refresh_from_db()
    assert user not in univ.moderators.all()
    assert not user.groups.filter(name="University Moderator").exists()
