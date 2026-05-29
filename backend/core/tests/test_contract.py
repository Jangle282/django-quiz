"""Contract-conformance tests for the generated OpenAPI schema (Phase 3.1).

These tests load ``api-contract.yaml`` and assert that drf-spectacular
produces a schema that matches the contract for the endpoints owned by the
current phase. Future phases extend the ``ENDPOINTS`` list as endpoints are
implemented so drift is caught immediately.
"""
from __future__ import annotations

from pathlib import Path

from django.http import HttpResponse
from typing import cast
import pytest
import yaml
from rest_framework.test import APIClient


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "api-contract.yaml"

# (path, method) pairs implemented so far. Extend as new endpoints land.
ENDPOINTS: list[tuple[str, str]] = [
    ("/api/health", "get"),
]


@pytest.fixture(scope="module")
def contract() -> dict:
    with CONTRACT_PATH.open() as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def generated_schema() -> dict:
    # drf-spectacular serves YAML by default; ask explicitly for JSON.
    response = cast(HttpResponse, APIClient().get("/api/schema", {"format": "json"}))
    assert response.status_code == 200, response.content
    return response.json()

# HUMAN NOTES: parameters come from fixtures methods / parametrize annotation - analoguous to phpunits data providers. 
@pytest.mark.parametrize("path,method", ENDPOINTS)
def test_generated_endpoint_matches_contract(
    contract: dict, generated_schema: dict, path: str, method: str
):
    contract_op = contract["paths"][path][method]
    generated_op = generated_schema["paths"][path][method]

    # operationId must match so client codegen stays stable.
    assert generated_op["operationId"] == contract_op["operationId"]

    # Tags must include every tag declared in the contract.
    contract_tags = set(contract_op.get("tags", []))
    generated_tags = set(generated_op.get("tags", []))
    assert contract_tags.issubset(generated_tags), (
        f"missing tags for {method.upper()} {path}: "
        f"{contract_tags - generated_tags}"
    )

    # Status codes from the contract must all be documented.
    contract_statuses = set(contract_op["responses"].keys())
    generated_statuses = set(generated_op["responses"].keys())
    assert contract_statuses.issubset(generated_statuses), (
        f"{method.upper()} {path} missing response codes: "
        f"{contract_statuses - generated_statuses}"
    )


def _resolve(schema: dict, node: dict) -> dict:
    """Follow a ``$ref`` one level if present, else return the node."""
    if "$ref" in node:
        ref = node["$ref"]
        assert ref.startswith("#/")
        parts = ref.lstrip("#/").split("/")
        resolved = schema
        for part in parts:
            resolved = resolved[part]
        return resolved
    return node


def test_health_response_schema_fields_match_contract(
    contract: dict, generated_schema: dict
):
    contract_props = contract["paths"]["/api/health"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["properties"]

    generated_response_schema = generated_schema["paths"]["/api/health"]["get"][
        "responses"
    ]["200"]["content"]["application/json"]["schema"]
    generated_props = _resolve(generated_schema, generated_response_schema)[
        "properties"
    ]

    assert set(contract_props.keys()) == set(generated_props.keys())
    # Timestamp must remain a date-time string in both.
    assert generated_props["timestamp"]["type"] == "string"
    assert generated_props["timestamp"].get("format") == "date-time"
    assert generated_props["status"]["type"] == "string"
