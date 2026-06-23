from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kamikonn_test",
        "USER": "kamikonn_user",
        "PASSWORD": "kamikonn_password",  # pragma: allowlist secret
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Disable rate limiting / throttling
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # type: ignore # noqa: F405
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    },
}
