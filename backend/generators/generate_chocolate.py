import pandas as pd
import numpy as np

np.random.seed(7)
n = 1000

# --- INGREDIENT RANGES ---
cocoa_solids  = np.random.uniform(35.0, 85.0, n)
cocoa_butter  = np.random.uniform(20.0, 40.0, n)
sugar         = np.random.uniform(5.0,  50.0, n)
milk_solids   = np.random.uniform(0.0,  25.0, n)
lecithin      = np.random.uniform(0.1,  0.5,  n)

noise = lambda: np.random.normal(0, 0.3, n)

# --- SENSORY EQUATIONS (rescaled to use full 1-10 range) ---

# Bitterness: high cocoa = very bitter; sugar and milk soften it
# cocoa_solids range 35-85 → after scaling should give 1-10
bitterness = (
    (cocoa_solids - 35) / 50 * 8 + 1   # maps 35→1, 85→9
    - 0.08 * sugar
    - 0.05 * milk_solids
    + noise()
)

# Sweetness: sugar 5-50% → maps to 1-10
sweetness = (
    (sugar - 5) / 45 * 8 + 1           # maps 5%→1, 50%→9
    + 0.04 * milk_solids
    - 0.02 * (cocoa_solids - 35) / 5
    + noise()
)

# Melt: cocoa butter 20-40% is the driver; non-linear (Form V crystals peak ~32%)
melt = (
    1 + 8 * np.exp(-0.5 * ((cocoa_butter - 32) / 6)**2)  # bell curve peaking at 32%
    + 0.5 * lecithin
    + noise()
)

# Snap: high cocoa solids + low cocoa butter + low sugar = better snap
snap = (
    (cocoa_solids - 35) / 50 * 5       # cocoa contributes up to 5 points
    - (cocoa_butter - 20) / 20 * 3     # high cocoa butter reduces snap
    - (sugar - 5) / 45 * 2             # high sugar reduces snap
    + 3                                 # base score
    + noise()
)

# Overall liking
overall_liking = (
    0.25 * sweetness
    + 0.20 * (10 - bitterness)
    + 0.30 * melt
    + 0.15 * snap
    + noise()
)

def clip(arr):
    return np.clip(arr, 1.0, 10.0).round(2)

df = pd.DataFrame({
    "cocoa_solids_pct":  cocoa_solids.round(3),
    "cocoa_butter_pct":  cocoa_butter.round(3),
    "sugar_pct":         sugar.round(3),
    "milk_solids_pct":   milk_solids.round(3),
    "lecithin_pct":      lecithin.round(3),
    "bitterness":        clip(bitterness),
    "sweetness":         clip(sweetness),
    "melt":              clip(melt),
    "snap":              clip(snap),
    "overall_liking":    clip(overall_liking),
})

df.to_csv("backend/data/chocolate.csv", index=False)
print(f"Chocolate dataset generated: {len(df)} rows")
print(df.head())
print(df.describe().round(2))