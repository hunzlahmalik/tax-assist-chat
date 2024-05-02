from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


class User(AbstractUser):
    email = models.EmailField(
        "email address",
        unique=True,
        help_text=_("Required. Inform a valid email address."),
        error_messages={
            "unique": _("A users with that email already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ["-id"]
