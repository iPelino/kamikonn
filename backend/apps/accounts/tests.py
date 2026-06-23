import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        kwargs.setdefault("password", "strongpassword123")  # pragma: allowlist secret
        kwargs.setdefault("first_name", "Test")
        kwargs.setdefault("last_name", "User")
        if "email" in kwargs and "username" not in kwargs:
            kwargs["username"] = kwargs["email"]
        user = User.objects.create_user(**kwargs)
        from allauth.account.models import EmailAddress

        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        return user

    return make_user


@pytest.mark.django_db
class TestAuthenticationEndpoints:
    def test_user_registration(self, api_client, mailoutbox):
        url = reverse("accounts:rest_register")
        data = {
            "email": "test@example.com",
            "password1": "securepassword123",  # pragma: allowlist secret
            "password2": "securepassword123",  # pragma: allowlist secret
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="test@example.com").exists()
        assert len(mailoutbox) == 1
        assert "test@example.com" in mailoutbox[0].to

    def test_user_login_unverified(self, api_client, create_user):
        user = create_user(
            email="unverified@example.com",
            password="mypassword123",  # pragma: allowlist secret
        )
        # Unverify the user
        EmailAddress.objects.filter(user=user).update(verified=False)

        url = reverse("accounts:token_obtain_pair")
        data = {
            "email": "unverified@example.com",
            "password": "mypassword123",  # pragma: allowlist secret
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "E-mail is not verified" in str(response.data["detail"])

    def test_user_registration_password_mismatch(self, api_client):
        url = reverse("accounts:rest_register")
        data = {
            "email": "test2@example.com",
            "password1": "securepassword123",  # pragma: allowlist secret
            "password2": "wrongpassword",  # pragma: allowlist secret
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password2" in response.data or "non_field_errors" in response.data

    def test_user_login(self, api_client, create_user):
        create_user(email="login@example.com", password="mypassword123")  # pragma: allowlist secret
        url = reverse("accounts:token_obtain_pair")
        data = {
            "email": "login@example.com",
            "password": "mypassword123",  # pragma: allowlist secret
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_user_profile_authenticated(self, api_client, create_user):
        user = create_user(
            email="profile@example.com",
            password="mypassword123",  # pragma: allowlist secret
        )
        api_client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_user_profile_unauthenticated(self, api_client):
        url = reverse("accounts:profile")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_logout(self, api_client, create_user):
        user = create_user(
            email="logout@example.com",
            password="mypassword123",  # pragma: allowlist secret
        )
        # Login to get refresh token
        login_url = reverse("accounts:token_obtain_pair")
        login_data = {
            "email": "logout@example.com",
            "password": "mypassword123",  # pragma: allowlist secret
        }
        login_response = api_client.post(login_url, login_data)
        refresh_token = login_response.data["refresh"]

        # Logout using the refresh token
        api_client.force_authenticate(user=user)
        logout_url = reverse("accounts:logout")
        response = api_client.post(logout_url, {"refresh": refresh_token})
        assert response.status_code == status.HTTP_205_RESET_CONTENT

        # Try to use refresh token again
        refresh_url = reverse("accounts:token_refresh")
        refresh_response = api_client.post(refresh_url, {"refresh": refresh_token})
        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
