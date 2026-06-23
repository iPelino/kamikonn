from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    # Optional: add a role field if needed later, but the plan mentioned:
    # "User Roles: User, Organizer (profile add-on flag), University Moderator, Admin."
    # We use groups for Univ Moderator & Admin, and a related profile for Organizer.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
