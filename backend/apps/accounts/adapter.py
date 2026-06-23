from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.http import JsonResponse
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("accounts:account_confirm_email", args=[emailconfirmation.key])
        return build_absolute_uri(request, url)

    def respond_email_verification_sent(self, request, user):
        return JsonResponse({"detail": "Verification e-mail sent."})
