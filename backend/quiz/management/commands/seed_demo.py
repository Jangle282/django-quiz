"""
Phase 2.3 seeder.

Usage::

    python manage.py seed_demo

Seeds the three required difficulties and a demo user with one game
containing one round of five questions, each with four answers
(one correct, one selected by the user).

Idempotent: re-running will not duplicate the difficulties / categories
or the demo user (factories use ``django_get_or_create``). Re-running
will however create an additional game for the demo user, which is
fine for local exploration but called out here for clarity.
"""
from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

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
from quiz.models import UserGame


class Command(BaseCommand):
    help = "Seed baseline lookup data and one demo game for local development."

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        DifficultyFactory(name="easy")
        medium = DifficultyFactory(name="medium")
        DifficultyFactory(name="hard")

        general_knowledge = CategoryFactory(name="General Knowledge")

        demo_user = UserFactory(username="demo")

        game = GameFactory(
            name="Demo Game",
            difficulty=medium,
            created_by=demo_user,
        )

        UserGameFactory(user=demo_user, game=game, role=UserGame.Role.HOST)

        round_one = RoundFactory(
            game=game,
            category=general_knowledge,
            round_number=1,
        )

        for question_index in range(5):
            question = QuestionFactory(
                round=round_one,
                question_text=f"Demo question {question_index + 1}?",
            )
            # 4 answers per question: one correct, the first marked as the
            # user's selection so results pages have data to render.
            for answer_index in range(4):
                AnswerFactory(
                    question=question,
                    answer_text=f"Q{question_index + 1} option {answer_index + 1}",
                    is_correct=(answer_index == 0),
                    user_selected=(answer_index == 0),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded demo user '{demo_user.username}' with game {game.id}."
            )
        )
