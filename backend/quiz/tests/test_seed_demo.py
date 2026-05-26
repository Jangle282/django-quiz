"""Tests for the Phase 2.3 seed_demo management command."""
from __future__ import annotations

from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from quiz.models import Answer, Difficulty, Game, Question, Round, UserGame


pytestmark = pytest.mark.django_db


def test_seed_demo_creates_required_fixtures():
    call_command("seed_demo", stdout=StringIO())

    assert set(Difficulty.objects.values_list("name", flat=True)) >= {
        "easy",
        "medium",
        "hard",
    }

    user = get_user_model().objects.get(username="demo")
    game = Game.objects.get(created_by=user)
    round_one = Round.objects.get(game=game, round_number=1)

    assert UserGame.objects.filter(
        user=user, game=game, role=UserGame.Role.HOST
    ).exists()
    assert Question.objects.filter(round=round_one).count() == 5
    assert Answer.objects.filter(question__round=round_one).count() == 20
    assert (
        Answer.objects.filter(question__round=round_one, is_correct=True).count() == 5
    )
