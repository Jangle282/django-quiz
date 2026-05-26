"""
Quiz domain models.

Phase 2.2 entities defined per agents/implementation_plan.md:
Difficulty, Game, UserGame, Category, Round, Question, Answer.

Cascade rules:
- Hierarchical ownership uses CASCADE so deleting a parent cleans up children:
  Game -> Round -> Question -> Answer, and Game -> UserGame.
- Lookup tables (Difficulty, Category) use PROTECT so we cannot accidentally
  orphan or destroy live games by removing a referenced lookup row.
- Game.created_by and UserGame.user use CASCADE: deleting a user removes
  their authored games and participation records (learning-project simplicity;
  a production system would likely soft-delete or anonymise instead).
"""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class Difficulty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "quiz_difficulty"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "quiz_category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.PROTECT,
        related_name="games",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_games",
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_games"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name or f"Game {self.id}"


class UserGame(models.Model):
    class Role(models.TextChoices):
        HOST = "host", "Host"
        PARTICIPANT = "participant", "Participant"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_games",
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="user_games",
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        db_table = "user_game"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"],
                name="uniq_user_game_membership",
            ),
        ]


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="rounds",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="rounds",
    )
    round_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_rounds"
        constraints = [
            models.UniqueConstraint(
                fields=["game", "round_number"],
                name="uniq_game_round_number",
            ),
        ]
        ordering = ["round_number"]


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.TextField()

    class Meta:
        db_table = "quiz_questions"
        ordering = ["id"]


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    answer_text = models.CharField(max_length=500)
    user_selected = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = "quiz_answers"
