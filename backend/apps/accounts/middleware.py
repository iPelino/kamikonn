from django.http import JsonResponse
from django_ratelimit.core import is_ratelimited


class AuthRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/auth/") and request.method == "POST":
            # Apply rate limiting to POST requests (login, register, reset password, etc.)
            # Rate: 10 requests per minute per IP
            ratelimited = is_ratelimited(
                request, group="auth_post", key="ip", rate="10/m", increment=True
            )
            if ratelimited:
                return JsonResponse(
                    {"detail": "Rate limit exceeded. Please try again later."}, status=429
                )

        return self.get_response(request)
