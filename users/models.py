from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import (
    ADMIN, USER, ANALYST, DATA_VIEWER
)


class User(AbstractUser):
    ROLES_TYPES = (
        (ADMIN, "Admin"),
        (USER, "User"),
        (ANALYST, "Analyst"),
        (DATA_VIEWER, "Data Viewer"),
    )

    role = models.CharField(max_length=255, choices=ROLES_TYPES, default=USER)

    def __str__(self) -> str:
        return str(self.username)
