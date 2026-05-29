"""URL routes owned by the ``core`` app (mounted under ``/api/``)."""
from __future__ import annotations

from django.urls import path

from core.views import HealthView

app_name = "core"

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
]
