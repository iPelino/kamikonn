from decouple import Csv, config

from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="kamikonn"),
        "USER": config("POSTGRES_USER", default="kamikonn_user"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="kamikonn_password"),
        "HOST": config("POSTGRES_HOST", default="db"),
        "PORT": config("POSTGRES_PORT", default="5432"),
    }
}

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
CORS_ALLOW_CREDENTIALS = True

# Production specific security settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files / Storage
# We will use DigitalOcean spaces for production
AWS_ACCESS_KEY_ID = config("DO_SPACES_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("DO_SPACES_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("DO_SPACES_BUCKET_NAME", default="")
AWS_S3_ENDPOINT_URL = config("DO_SPACES_ENDPOINT_URL", default="")
AWS_S3_REGION_NAME = config("DO_SPACES_REGION", default="fra1")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_LOCATION = "media"  # optional, if media files should be in a subfolder
AWS_DEFAULT_ACL = "public-read"

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
}

# Email
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
    },
}
