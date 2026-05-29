"""Project-wide throttle classes.

Centralised here so individual views never instantiate ad-hoc throttle logic
and so global defaults remain the single source of truth (see settings.py).
"""
from __future__ import annotations

from rest_framework.throttling import SimpleRateThrottle


class HealthCheckThrottle(SimpleRateThrottle):
    """Anon-friendly throttle for the public liveness endpoint.

    Rate lives in ``REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['health']`` so
    operators can tune it without touching code.
    """

    scope = "health"

    def get_cache_key(self, request, view):
        # Liveness is unauthenticated; throttle per client IP.
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
