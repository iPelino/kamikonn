import uuid

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory(django_user_model):
    def create_user(**kwargs):
        username = kwargs.pop("username", f"testuser_{uuid.uuid4().hex[:8]}")
        email = kwargs.pop("email", f"{username}@example.com")
        password = kwargs.pop("password", "testpassword123")  # pragma: allowlist secret
        return django_user_model.objects.create_user(
            username=username, email=email, password=password, **kwargs
        )

    return create_user
