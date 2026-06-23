import os

from decouple import config

# Default to development
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", default="kamikonn.settings.development"),
)  # noqa: E501
