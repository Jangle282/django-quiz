"""Response/request schema definitions kept out of views.

Per the project standards in ``agents/AGENTS.md``, request and response
schemas live next to their app so views stay slim and Swagger docs are
generated from these classes rather than inline view decorators.
"""
from __future__ import annotations

from rest_framework import serializers


class HealthResponseSerializer(serializers.Serializer):
    """Shape returned by ``GET /api/health``.

    Mirrors ``/api/health`` in ``api-contract.yaml``.
    """

    status = serializers.CharField()
    timestamp = serializers.DateTimeField()
