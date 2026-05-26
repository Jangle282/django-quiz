"""Unit tests for the custom User model (Phase 2.2)."""
from __future__ import annotations

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_user_has_uuid_primary_key():
    user = UserFactory()

    assert isinstance(user.id, uuid.UUID)


def test_username_is_unique():
    UserFactory(username="alice")

    with pytest.raises(IntegrityError):
        # Bypass the factory's get_or_create so we actually hit the DB constraint.
        get_user_model().objects.create(username="alice")


def test_password_is_hashed_not_stored_plaintext():
    user = UserFactory(password="P@ssword12345")

    assert user.password != "P@ssword12345"
    assert user.check_password("P@ssword12345")


def test_timestamps_are_set_on_create_and_update():
    user = UserFactory()
    created = user.created_at
    original_updated = user.updated_at

    user.username = "renamed"
    user.save()

    assert user.created_at == created
    assert user.updated_at >= original_updated


def test_user_table_name():
    assert get_user_model()._meta.db_table == "users"
