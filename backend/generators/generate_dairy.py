import pandas as pd
import numpy as np

np.random.seed(42)
n = 1500

# --- INGREDIENT RANGES ---
fat         = np.random.uniform(0.5, 8.0, n)
protein     = np.random.uniform(3.0, 6.0, n)
sugar       = np.random.uniform(0.0, 12.0, n)
starter     = np.random.uniform(1.0, 4.0, n)
stabilizer  = np.random.uniform(0.0, 1.0, n)

noise = lambda: np.random.normal(0, 0.3, n)

# --- SENSORY EQUATIONS (food science grounded) ---

# Sweetness: driven almost entirely by sugar
sweetness = (
    0.7 * sugar
    + 0.05 * fat
    + noise()
)

# Sourness: lactic acid from starter culture; fat dampens sourness
sourness = (
    1.8 * starter
    - 0.15 * fat
    - 0.05 * sugar
    + noise()
)

# Body: fat + protein + stabilizer interaction term
body = (
    0.4 * fat
    + 0.5 * protein
    + 2.5 * stabilizer
    + 0.15 * fat * stabilizer   # interaction: stabilizer works better with fat
    + noise()
)

# Creaminess: fat is the dominant driver, protein supports
creaminess = (
    0.7 * fat
    + 0.2 * protein
    + 1.5 * stabilizer
    + noise()
)

# Flavor balance: measures how well the taste components work together
# Peaks when sweetness and sourness are moderate and body is present
flavor_balance = (
    0.20 * sweetness
    + 0.15 * (10 - np.abs(sourness - 5))   # best when sourness is moderate
    + 0.25 * body
    + 0.25 * creaminess
    + 0.10 * np.minimum(sweetness, creaminess)  # synergy term
    + noise()
)

# --- CLIP ALL SCORES TO 1-10 SCALE ---
def clip(arr):
    return np.clip(arr, 1.0, 10.0).round(2)

df = pd.DataFrame({
    "fat_pct":          fat.round(3),
    "protein_pct":      protein.round(3),
    "sugar_pct":        sugar.round(3),
    "starter_pct":      starter.round(3),
    "stabilizer_pct":   stabilizer.round(3),
    "sweetness":        clip(sweetness),
    "sourness":         clip(sourness),
    "body":             clip(body),
    "creaminess":       clip(creaminess),
    "flavor_balance":   clip(flavor_balance),
})

df.to_csv("backend/data/dairy.csv", index=False)
print(f"Dairy dataset generated: {len(df)} rows")
print(df.head())
print(df.describe().round(2))
