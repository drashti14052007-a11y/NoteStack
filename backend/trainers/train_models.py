import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error

os.makedirs("backend/models", exist_ok=True)

CATEGORIES = {
    "dairy": {
        "file": "backend/data/dairy.csv",
        "features": ["fat_pct", "protein_pct", "sugar_pct", "starter_pct", "stabilizer_pct"],
        "targets":  ["sweetness", "sourness", "body", "creaminess", "flavor_balance"],
    },
    "chocolate": {
        "file": "backend/data/chocolate.csv",
        "features": ["cocoa_solids_pct", "cocoa_butter_pct", "sugar_pct", "milk_solids_pct", "lecithin_pct"],
        "targets":  ["bitterness", "sweetness", "melt", "snap", "flavor_balance"],
    },
    "spices": {
        "file": "backend/data/spices.csv",
        "features": ["chili_pct", "cumin_pct", "coriander_pct", "turmeric_pct", "salt_pct"],
        "targets":  ["pungency", "aroma", "colour", "saltiness", "flavor_balance"],
    },
    "snacks": {
        "file": "backend/data/snacks.csv",
        "features": ["starch_pct", "fat_pct", "salt_pct", "moisture_pct", "seasoning_pct"],
        "targets":  ["crunchiness", "oiliness", "saltiness", "flavour", "flavor_balance"],
    },
}

for name, config in CATEGORIES.items():
    print(f"\n{'='*50}")
    print(f"Training: {name.upper()}")
    print(f"{'='*50}")

    df = pd.read_csv(config["file"])
    X = df[config["features"]].values
    y = df[config["targets"]].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        )
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2  = r2_score(y_test, y_pred, multioutput="uniform_average")
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"R² score  : {r2:.4f}  (closer to 1.0 = better)")
    print(f"RMSE      : {rmse:.4f}  (lower = better)")
    print(f"Features  : {config['features']}")
    print(f"Targets   : {config['targets']}")

    model_path = f"backend/models/{name}_model.joblib"
    joblib.dump({
        "model":    model,
        "features": config["features"],
        "targets":  config["targets"],
    }, model_path)

    print(f"Saved -> {model_path}")

print("\nAll 4 models trained and saved.")