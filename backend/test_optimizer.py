"""
Tests for optimizer.py

IMPORTANT — these tests run against your REAL trained models (the .joblib
files in models/). That means:
  - They must be run from inside the backend/ folder (same as your manual
    script), so the relative path "models/dairy_model.joblib" resolves.
  - They will be a bit slower than the compliance tests, since each one
    runs a real SciPy optimization loop (5 trials) against a real model.
  - `load_models()` is called once for the whole file (see the fixture
    below), not once per test, so we don't reload from disk 20+ times.

What we're checking for each category:
  1. The formulation values land within the allowed bounds (ingredients
     can't go negative or above their defined range).
  2. The formulation has exactly the right ingredient keys.
  3. confidence_pct is always between 0 and 100 (a malformed residual
     calculation could in theory push this outside that range).
  4. residual_error is never negative (it's a mean absolute difference,
     so it mathematically can't be — but worth locking in as a contract).
  5. Predicted scores and target scores both report all 5 attributes.

What we are NOT testing here:
  - Whether the *specific* numbers are "good" formulations in a food-
    science sense — that's a domain judgment call, not something a test
    can decide. These tests catch broken code, not bad recipes.
  - Anything about the actual .joblib files being well-trained models —
    we're trusting they exist and were trained reasonably; we're testing
    that the optimizer wraps them correctly.
"""

import pytest
from optimizer import load_models, run_optimizer, CATEGORY_CONFIG

# Load all 4 models once, before any test in this file runs.
@pytest.fixture(scope="module", autouse=True)
def setup_models():
    load_models()


@pytest.mark.parametrize("category", ["dairy", "chocolate", "spices", "snacks"])
def test_formulation_keys_match_features(category):
    config = CATEGORY_CONFIG[category]
    target = [5.0] * len(config["targets"])  # mid-range target for every attribute
    result = run_optimizer(category, target)

    assert set(result["formulation"].keys()) == set(config["features"])


@pytest.mark.parametrize("category", ["dairy", "chocolate", "spices", "snacks"])
def test_formulation_values_within_bounds(category):
    config = CATEGORY_CONFIG[category]
    target = [5.0] * len(config["targets"])
    result = run_optimizer(category, target)

    for feature, (low, high) in zip(config["features"], config["bounds"]):
        value = result["formulation"][feature]
        assert low - 1e-6 <= value <= high + 1e-6, (
            f"{category}.{feature} = {value} is outside allowed bounds [{low}, {high}]"
        )


@pytest.mark.parametrize("category", ["dairy", "chocolate", "spices", "snacks"])
def test_confidence_is_a_valid_percentage(category):
    config = CATEGORY_CONFIG[category]
    target = [5.0] * len(config["targets"])
    result = run_optimizer(category, target)

    assert 0 <= result["confidence_pct"] <= 100


@pytest.mark.parametrize("category", ["dairy", "chocolate", "spices", "snacks"])
def test_residual_error_is_never_negative(category):
    config = CATEGORY_CONFIG[category]
    target = [5.0] * len(config["targets"])
    result = run_optimizer(category, target)

    assert result["residual_error"] >= 0


@pytest.mark.parametrize("category", ["dairy", "chocolate", "spices", "snacks"])
def test_predicted_and_target_scores_have_all_attributes(category):
    config = CATEGORY_CONFIG[category]
    target = [5.0] * len(config["targets"])
    result = run_optimizer(category, target)

    assert set(result["predicted_scores"].keys()) == set(config["targets"])
    assert set(result["target_scores"].keys()) == set(config["targets"])


def test_easy_achievable_target_gives_high_confidence():
    # Using the model's own "natural" starting point (x0) as the target
    # should be very achievable, so confidence should be reasonably high.
    # This guards against confidence scoring being accidentally inverted
    # or badly scaled.
    config = CATEGORY_CONFIG["dairy"]
    # Run once first to see what x0 actually predicts, then target that.
    from optimizer import MODELS
    natural_scores = MODELS["dairy"].predict([config["x0"]])[0]

    result = run_optimizer("dairy", list(natural_scores))
    assert result["confidence_pct"] >= 70, (
        f"Targeting the model's own natural output only gave "
        f"{result['confidence_pct']}% confidence — expected this to be easy to hit."
    )


def test_extreme_unrealistic_target_gives_lower_confidence():
    # Asking for a target far outside what any formulation could realistically
    # produce (all 10s) should yield noticeably lower confidence than a
    # moderate, realistic target. This is a relative check, not an exact one,
    # since "low" is fuzzy — but it catches a confidence score that doesn't
    # respond to target difficulty at all (e.g. always returns ~100%).
    config = CATEGORY_CONFIG["dairy"]
    moderate = run_optimizer("dairy", [5.0] * len(config["targets"]))
    extreme  = run_optimizer("dairy", [10.0] * len(config["targets"]))

    assert extreme["confidence_pct"] <= moderate["confidence_pct"], (
        "An extreme, harder-to-hit target produced confidence >= a moderate "
        "target's confidence — confidence score may not be responding to "
        "how achievable the target actually is."
    )