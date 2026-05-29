"""Cross-cutting API views (health, etc.).

Views are kept slim. The health endpoint has no business logic to delegate,
so it lives directly here.
"""
from __future__ import annotations

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import HealthResponseSerializer
from core.throttling import HealthCheckThrottle


class HealthView(APIView):
    """Unauthenticated liveness/readiness probe.

    Matches ``GET /api/health`` in ``api-contract.yaml``.
    """

    authentication_classes: list = []
    permission_classes = [AllowAny]
    throttle_classes = [HealthCheckThrottle]

    @extend_schema(
        operation_id="get_api_health",
        tags=["Health"],
        summary="Health check",
        responses={200: HealthResponseSerializer},
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        payload = {"status": "ok", "timestamp": timezone.now()}
        data = HealthResponseSerializer(payload).data
        return Response(data, status=status.HTTP_200_OK)
