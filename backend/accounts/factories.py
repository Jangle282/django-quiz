"""Factories for the accounts app. Used by tests and the seed command."""
from __future__ import annotations

from typing import cast

import factory
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")

    @factory.post_generation
    def password(self, created, extracted, **kwargs):
        if not created:
            return
        user = cast(User, self)
        user.set_password(extracted or "P@ssword12345")
        user.save()
