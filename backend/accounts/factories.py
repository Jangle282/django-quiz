"""Factories for the accounts app. Used by tests and the seed command."""
from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "P@ssword12345")
        user = model_class(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user
