"""Factories for the quiz app. Used by tests and the seed command."""
from __future__ import annotations

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Answer, Category, Difficulty, Game, Question, Round, UserGame


class DifficultyFactory(DjangoModelFactory):
    class Meta:
        model = Difficulty
        django_get_or_create = ("name",)

    name = factory.Iterator(["easy", "medium", "hard"])


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = "General Knowledge"


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    name = factory.Sequence(lambda n: f"Game {n}")
    difficulty = factory.SubFactory(DifficultyFactory)
    created_by = factory.SubFactory(UserFactory)
    started_at = factory.LazyFunction(timezone.now)


class UserGameFactory(DjangoModelFactory):
    class Meta:
        model = UserGame

    user = factory.SubFactory(UserFactory)
    game = factory.SubFactory(GameFactory)
    role = UserGame.Role.PARTICIPANT


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    game = factory.SubFactory(GameFactory)
    category = factory.SubFactory(CategoryFactory)
    round_number = factory.Sequence(lambda n: n + 1)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    round = factory.SubFactory(RoundFactory)
    question_text = factory.Sequence(lambda n: f"Sample question {n}?")


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    answer_text = factory.Sequence(lambda n: f"Answer {n}")
    user_selected = False
    is_correct = False
