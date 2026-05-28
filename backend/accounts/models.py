"""
Custom User model.

Phase 2.2 requirements (see agents/implementation_plan.md):
- table name: users
- entity name: User
- columns: id (uuid PK), username (unique), password (hashed),
  created_at, updated_at

We extend Django's AbstractBaseUser + PermissionsMixin so password hashing
and the standard auth machinery still work, but we replace the integer PK
with a UUID and omit Django's default first_name/last_name/email fields
since the plan does not require them.
"""
from __future__ import annotations

import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager providing create_user / create_superuser using username only."""

    use_in_migrations = True

    def _create_user(self, username: str, password: str | None, **extra_fields):
        if not username:
            raise ValueError("Username must be provided")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=180, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.username
