"""
Tests for main.py — the actual API endpoints.

How this is different from test_compliance.py and test_optimizer.py:
- Those tested your Python functions directly (check_compliance(),
  run_optimizer()). This file tests the HTTP layer on top of them — the
  actual routes your frontend calls (/formulate, /report, /categories,
  /history). It catches a different kind of bug: e.g. a typo in a route
  path, a request body that doesn't match what FastAPI expects, or a
  status code that's wrong even though the underlying logic is fine.

How TestClient works, in plain terms:
- `client.get("/categories")` and `client.post("/formulate", json={...})`
  simulate real HTTP requests against your FastAPI app, in-memory — no
  need to have `uvicorn` running separately. It exercises the *real*
  code path: routing, validation, your optimizer, your compliance
  checker, and your real SQLite database (history.db).

A note on side effects:
- Every successful /formulate call writes a row to history.db. Because
  of that, test_history_count_increases_after_formulate checks that the
  count goes UP BY ONE, rather than checking for an exact total — an
  exact number would break the moment you'd run the tests twice, or had
  used the app manually before running tests.

Run this from inside backend/, same as the other test files:
    pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# `with TestClient(app) as client:` triggers FastAPI's startup event,
# which is what actually calls load_models() — without `with`, the
# models never get loaded and every /formulate call would fail.
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ── Root + categories ────────────────────────────────────────

def test_root_returns_running_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_categories_returns_all_four(client):
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"dairy", "chocolate", "spices", "snacks"}


def test_categories_each_have_features_targets_bounds(client):
    response = client.get("/categories")
    data = response.json()
    for category, config in data.items():
        assert "features" in config
        assert "targets" in config
        assert "bounds" in config
        assert len(config["features"]) == len(config["bounds"])


# ── /formulate — happy path ──────────────────────────────────

@pytest.mark.parametrize("category,n_targets", [
    ("dairy", 5), ("chocolate", 5), ("spices", 5), ("snacks", 5),
])
def test_formulate_valid_request_succeeds(client, category, n_targets):
    response = client.post("/formulate", json={
        "category": category,
        "target_scores": [5.0] * n_targets,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == category
    assert "formulation" in data
    assert "compliance" in data
    assert "status" in data["compliance"]


def test_formulate_is_case_insensitive_on_category(client):
    # main.py does request.category.lower(), so "DAIRY" should work
    # exactly the same as "dairy".
    response = client.post("/formulate", json={
        "category": "DAIRY",
        "target_scores": [5.0] * 5,
    })
    assert response.status_code == 200
    assert response.json()["category"] == "dairy"


def test_formulate_response_includes_compliance_block(client):
    response = client.post("/formulate", json={
        "category": "snacks",
        "target_scores": [5.0] * 5,
    })
    compliance = response.json()["compliance"]
    assert compliance["status"] in ("COMPLIANT", "ADVISORY", "NON-COMPLIANT")
    assert "passed" in compliance
    assert "warnings" in compliance
    assert "flags" in compliance


# ── /formulate — error handling ──────────────────────────────

def test_formulate_unknown_category_returns_400(client):
    response = client.post("/formulate", json={
        "category": "bakery",
        "target_scores": [5.0, 5.0, 5.0, 5.0, 5.0],
    })
    assert response.status_code == 400
    assert "Unknown category" in response.json()["detail"]


def test_formulate_wrong_number_of_target_scores_returns_400(client):
    # dairy expects exactly 5 target scores; sending 3 should be rejected
    # with a clear error, not crash or silently misbehave.
    response = client.post("/formulate", json={
        "category": "dairy",
        "target_scores": [5.0, 5.0, 5.0],
    })
    assert response.status_code == 400
    assert "Expected" in response.json()["detail"]


def test_formulate_missing_category_field_returns_422():
    # Pydantic validation error (missing required field) — FastAPI
    # returns 422, not 400, for this kind of malformed request.
    # Using a fresh client without triggering startup is fine here since
    # this never reaches the route logic — it fails validation first.
    from fastapi.testclient import TestClient as TC
    with TC(app) as c:
        response = c.post("/formulate", json={
            "target_scores": [5.0, 5.0, 5.0, 5.0, 5.0],
        })
        assert response.status_code == 422


def test_formulate_target_scores_wrong_type_returns_422(client):
    # Sending strings instead of numbers should fail Pydantic validation.
    response = client.post("/formulate", json={
        "category": "dairy",
        "target_scores": ["high", "low", "medium", "high", "low"],
    })
    assert response.status_code == 422


# ── /report ────────────────────────────────────────────────────

def test_report_returns_pdf_bytes(client):
    response = client.post("/report", json={
        "category": "dairy",
        "target_scores": [5.0] * 5,
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content[:4] == b"%PDF"  # real PDF files start with this signature


def test_report_unknown_category_returns_400(client):
    response = client.post("/report", json={
        "category": "bakery",
        "target_scores": [5.0] * 5,
    })
    assert response.status_code == 400


# ── /history ───────────────────────────────────────────────────

def test_history_count_increases_after_formulate(client):
    before = client.get("/history?limit=1000").json()
    count_before = len(before)

    client.post("/formulate", json={
        "category": "spices",
        "target_scores": [5.0] * 5,
    })

    after = client.get("/history?limit=1000").json()
    count_after = len(after)

    assert count_after == count_before + 1


def test_history_records_have_expected_fields(client):
    response = client.get("/history?limit=1")
    records = response.json()
    if records:  # only check shape if there's at least one record
        record = records[0]
        assert "id" in record
        assert "category" in record
        assert "confidence_pct" in record
        assert "compliance_status" in record
        assert "created_at" in record
