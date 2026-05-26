"""Unit tests for the quiz domain models (Phase 2.2)."""
from __future__ import annotations

import uuid

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from accounts.factories import UserFactory
from quiz.factories import (
    AnswerFactory,
    CategoryFactory,
    DifficultyFactory,
    GameFactory,
    QuestionFactory,
    RoundFactory,
    UserGameFactory,
)
from quiz.models import Answer, Game, Question, Round, UserGame


pytestmark = pytest.mark.django_db


def test_all_models_use_uuid_primary_keys():
    objects = [
        DifficultyFactory(),
        CategoryFactory(),
        GameFactory(),
        UserGameFactory(),
        RoundFactory(),
        QuestionFactory(),
        AnswerFactory(),
    ]
    for obj in objects:
        assert isinstance(obj.id, uuid.UUID), type(obj).__name__


def test_table_names_match_plan():
    assert Game._meta.db_table == "quiz_games"
    assert UserGame._meta.db_table == "user_game"
    assert Round._meta.db_table == "quiz_rounds"
    assert Question._meta.db_table == "quiz_questions"
    assert Answer._meta.db_table == "quiz_answers"


def test_difficulty_is_protected_from_deletion_when_in_use():
    difficulty = DifficultyFactory(name="medium")
    GameFactory(difficulty=difficulty)

    with pytest.raises(ProtectedError):
        difficulty.delete()


def test_deleting_game_cascades_rounds_questions_answers_and_memberships():
    game = GameFactory()
    UserGameFactory(game=game)
    round_one = RoundFactory(game=game)
    question = QuestionFactory(round=round_one)
    AnswerFactory(question=question)

    game.delete()

    assert not Round.objects.filter(game_id=game.id).exists()
    assert not Question.objects.filter(round_id=round_one.id).exists()
    assert not Answer.objects.filter(question_id=question.id).exists()
    assert not UserGame.objects.filter(game_id=game.id).exists()


def test_deleting_user_cascades_their_games_and_memberships():
    user = UserFactory()
    game = GameFactory(created_by=user)
    UserGameFactory(user=user, game=game, role=UserGame.Role.HOST)

    user.delete()

    assert not Game.objects.filter(id=game.id).exists()


def test_user_cannot_join_same_game_twice():
    user = UserFactory()
    game = GameFactory()
    UserGameFactory(user=user, game=game, role=UserGame.Role.HOST)

    with pytest.raises(IntegrityError):
        UserGame.objects.create(user=user, game=game, role=UserGame.Role.PARTICIPANT)


def test_round_numbers_are_unique_within_a_game():
    game = GameFactory()
    RoundFactory(game=game, round_number=1)

    with pytest.raises(IntegrityError):
        Round.objects.create(
            game=game,
            category=CategoryFactory(),
            round_number=1,
        )


def test_game_name_and_completed_at_are_optional():
    game = GameFactory(name=None)

    assert game.name is None
    assert game.completed_at is None
