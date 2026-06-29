import numpy as np
import joblib
from scipy.optimize import minimize

MODELS = {}

CATEGORY_CONFIG = {
    "dairy": {
        "features": ["fat_pct", "protein_pct", "sugar_pct", "starter_pct", "stabilizer_pct"],
        "targets":  ["sweetness", "sourness", "body", "creaminess", "overall_liking"],
        "bounds":   [(0.5, 8.0), (3.0, 6.0), (0.0, 12.0), (1.0, 4.0), (0.0, 1.0)],
        "x0":       [4.0, 4.5, 6.0, 2.5, 0.5],
    },
    "chocolate": {
        "features": ["cocoa_solids_pct", "cocoa_butter_pct", "sugar_pct", "milk_solids_pct", "lecithin_pct"],
        "targets":  ["bitterness", "sweetness", "melt", "snap", "overall_liking"],
        "bounds":   [(35.0, 85.0), (20.0, 40.0), (5.0, 50.0), (0.0, 25.0), (0.1, 0.5)],
        "x0":       [60.0, 30.0, 27.0, 12.0, 0.3],
    },
    "spices": {
        "features": ["chili_pct", "cumin_pct", "coriander_pct", "turmeric_pct", "salt_pct"],
        "targets":  ["pungency", "aroma", "colour", "saltiness", "overall_liking"],
        "bounds":   [(0.0, 40.0), (0.0, 30.0), (0.0, 30.0), (0.0, 15.0), (0.0, 10.0)],
        "x0":       [20.0, 15.0, 15.0, 7.5, 5.0],
    },
    "snacks": {
        "features": ["starch_pct", "fat_pct", "salt_pct", "moisture_pct", "seasoning_pct"],
        "targets":  ["crunchiness", "oiliness", "saltiness", "flavour", "overall_liking"],
        "bounds":   [(40.0, 70.0), (10.0, 35.0), (0.5, 4.0), (1.0, 8.0), (0.0, 8.0)],
        "x0":       [55.0, 22.0, 2.0, 4.0, 4.0],
    },
}


def load_models():
    for cat in CATEGORY_CONFIG:
        MODELS[cat] = joblib.load(f"models/{cat}_model.joblib")["model"]

def run_optimizer(category: str, target_scores: list[float]) -> dict:
    config = CATEGORY_CONFIG[category]
    model  = MODELS[category]
    target = np.array(target_scores)

    def objective(x):
        pred = model.predict([x])[0]
        return float(np.sum((pred - target) ** 2))

    best_result = None
    best_val    = float("inf")

    # Run optimizer 5 times from different starting points for robustness
    for trial in range(5):
        x0 = np.array(config["x0"]) + np.random.normal(0, 0.5, len(config["x0"]))
        x0 = np.clip(x0, [b[0] for b in config["bounds"]], [b[1] for b in config["bounds"]])

        result = minimize(
            objective,
            x0,
            method="SLSQP",
            bounds=config["bounds"],
            options={"maxiter": 1000, "ftol": 1e-9},
        )

        if result.fun < best_val:
            best_val    = result.fun
            best_result = result

    x_opt        = best_result.x
    pred_scores  = model.predict([x_opt])[0]
    residual     = np.mean(np.abs(pred_scores - target))
    confidence   = round(float(max(0, 1 - residual / 5) * 100), 1)

    return {
        "formulation": {
            feat: round(float(val), 3)
            for feat, val in zip(config["features"], x_opt)
        },
        "predicted_scores": {
            tgt: round(float(val), 2)
            for tgt, val in zip(config["targets"], pred_scores)
        },
        "target_scores": {
            tgt: round(float(val), 2)
            for tgt, val in zip(config["targets"], target)
        },
        "confidence_pct": confidence,
        "residual_error": round(float(residual), 4),
    }