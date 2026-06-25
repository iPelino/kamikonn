import io

import pytest
from django.urls import reverse
from rest_framework import status

from apps.events.models import Event, EventStatus

pytestmark = pytest.mark.django_db


def test_import_csv_unauthenticated(api_client):
    url = reverse("event-import-csv")
    response = api_client.post(url, {})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_import_csv_success(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    csv_content = """title,description,start_time,end_time,location,is_virtual,capacity,price
Event 1,Test desc 1,2026-10-10T10:00:00Z,2026-10-10T12:00:00Z,Kigali,false,100,0.00
Event 2,Test desc 2,2026-11-10T10:00:00Z,2026-11-10T12:00:00Z,,true,50,15.50
"""
    file_obj = io.BytesIO(csv_content.encode("utf-8"))
    file_obj.name = "events.csv"

    url = reverse("event-import-csv")
    response = api_client.post(url, {"file": file_obj}, format="multipart")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["events_created"] == 2
    assert len(response.data["errors"]) == 0

    events = Event.objects.all().order_by("title")
    assert events.count() == 2

    assert events[0].title == "Event 1"
    assert events[0].location == "Kigali"
    assert not events[0].is_virtual
    assert events[0].capacity == 100
    assert events[0].price == 0.00
    assert events[0].status == EventStatus.DRAFT

    assert events[1].title == "Event 2"
    assert events[1].location == ""
    assert events[1].is_virtual
    assert events[1].capacity == 50
    assert events[1].price == 15.50
    assert events[1].status == EventStatus.DRAFT


def test_import_csv_missing_title(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    csv_content = """title,description,start_time,end_time,location,is_virtual,capacity,price
,Test desc 1,2026-10-10T10:00:00Z,2026-10-10T12:00:00Z,Kigali,false,100,0.00
Event 2,Test desc 2,2026-11-10T10:00:00Z,2026-11-10T12:00:00Z,,true,50,15.50
"""
    file_obj = io.BytesIO(csv_content.encode("utf-8"))
    file_obj.name = "events.csv"

    url = reverse("event-import-csv")
    response = api_client.post(url, {"file": file_obj}, format="multipart")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["events_created"] == 1
    assert len(response.data["errors"]) == 1
    assert "Row 1: Missing title" in response.data["errors"][0]

    assert Event.objects.count() == 1
