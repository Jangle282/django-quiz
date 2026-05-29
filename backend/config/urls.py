"""Root URL configuration.

API routes are mounted under ``/api/`` to match the frontend client
(``VITE_API_BASE_URL=http://localhost:8080/api``) and the OpenAPI contract.
"""
from __future__ import annotations

from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_urlpatterns = [
    path("", include("core.urls")),
    # Schema + Swagger UI live under /api/ so they share the same base URL
    # as the rest of the API while remaining outside the contract.
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = [
    path("api/", include(api_urlpatterns)),
]
