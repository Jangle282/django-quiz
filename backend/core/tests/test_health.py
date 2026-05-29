"""Feature tests for ``GET /api/health`` (Phase 3.1).

Covers:
* response shape (status + ISO-8601 timestamp) matching ``api-contract.yaml``
* unauthenticated access (no Authorization header required)
* scoped throttle kicks in after the configured rate

These are full request/response tests via DRF's ``APIClient`` per the repo
testing standards (real DB, no business-logic mocking).
"""
from __future__ import annotations

from datetime import datetime
from typing import cast

from django.http import HttpResponse
import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


HEALTH_URL = "/api/health"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(autouse=True)
def _reset_throttle_cache():
    """DRF throttles use the default cache; clear between tests."""
    cache.clear()
    yield
    cache.clear()


def test_health_endpoint_reverse_matches_contract_path():
    # If someone renames the URL we want the contract path to keep working.
    # HUMAN NOTES: reverse() analoguous to route(). core:health is <app_name>:<route_name>.
    assert reverse("core:health") == HEALTH_URL


def test_health_returns_200_and_expected_shape(api_client: APIClient):
    response = cast(HttpResponse, api_client.get(HEALTH_URL))

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert set(body.keys()) == {"status", "timestamp"}
    assert body["status"] == "ok"
    # Must be a valid ISO-8601 datetime (drops trailing 'Z' for fromisoformat).
    parsed = datetime.fromisoformat(body["timestamp"].replace("Z", "+00:00"))
    assert parsed.tzinfo is not None


def test_health_is_unauthenticated(api_client: APIClient):
    # No Authorization header set; must still succeed.
    response = cast(HttpResponse, api_client.get(HEALTH_URL))
    assert response.status_code == status.HTTP_200_OK


def test_health_endpoint_is_throttled(api_client: APIClient, monkeypatch):
    # DRF caches ``DEFAULT_THROTTLE_RATES`` onto ``SimpleRateThrottle.THROTTLE_RATES``
    # at import time, so a settings override would not affect the rate. Patch the
    # class dict directly instead.
    from core.throttling import HealthCheckThrottle

    monkeypatch.setitem(HealthCheckThrottle.THROTTLE_RATES, "health", "2/min")

    assert cast(HttpResponse, api_client.get(HEALTH_URL)).status_code == status.HTTP_200_OK
    assert cast(HttpResponse, api_client.get(HEALTH_URL)).status_code == status.HTTP_200_OK
    throttled = cast(HttpResponse, api_client.get(HEALTH_URL))

    assert throttled.status_code == status.HTTP_429_TOO_MANY_REQUESTS
