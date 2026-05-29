from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Cross-cutting endpoints (health, schema) and shared infra."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
