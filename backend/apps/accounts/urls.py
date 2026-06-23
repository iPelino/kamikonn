from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ConfirmEmailRedirectView,
    CustomTokenObtainPairView,
    GoogleLogin,
    LogoutView,
    UserProfileView,
)

app_name = "accounts"

urlpatterns = [
    # Custom endpoints (take precedence)
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    # dj-rest-auth overrides (or additions)
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "registration/account-confirm-email/<str:key>/",
        ConfirmEmailRedirectView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "registration/verify-email/",
        VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
