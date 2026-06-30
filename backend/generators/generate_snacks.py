import pandas as pd
import numpy as np

np.random.seed(21)
n = 1000

# --- INGREDIENT RANGES ---
starch_pct   = np.random.uniform(40.0, 70.0, n)   # base starch (potato/corn) %
fat_pct      = np.random.uniform(10.0, 35.0, n)   # frying fat %
salt_pct     = np.random.uniform(0.5,   4.0, n)   # salt %
moisture_pct = np.random.uniform(1.0,   8.0, n)   # residual moisture after frying %
seasoning_pct= np.random.uniform(0.0,   8.0, n)   # flavour seasoning %

noise = lambda: np.random.normal(0, 0.3, n)

# --- SENSORY EQUATIONS ---

# Crunchiness: moisture is the key driver — NON-LINEAR threshold effect
# Above 4% moisture, crunchiness drops sharply (real extrusion food science)
crunchiness = (
    9 - 1.5 * moisture_pct                        # base: drops with moisture
    - 2.0 * np.maximum(0, moisture_pct - 4.0)     # extra penalty above 4% threshold
    + 0.05 * starch_pct * 0.1
    + noise()
)

# Oiliness: fat % drives this directly
oiliness = (
    (fat_pct - 10) / 25 * 8 + 1                   # maps 10%→1, 35%→9
    + noise()
)

# Saltiness: direct relationship
saltiness = (
    (salt_pct - 0.5) / 3.5 * 8 + 1               # maps 0.5%→1, 4%→9
    + noise()
)

# Flavour intensity: seasoning drives this
flavour = (
    (seasoning_pct / 8) * 8 + 1                   # maps 0%→1, 8%→9
    + 0.1 * saltiness                              # salt enhances flavour perception
    + noise()
)

# Flavor balance: measures how well all taste/texture components work together
# Best when crunchy, well-seasoned, moderately salty, and not too oily
flavor_balance = (
    0.25 * crunchiness
    + 0.25 * flavour
    + 0.15 * saltiness
    + 0.15 * (10 - oiliness)                      # too oily = less balanced
    + 0.10 * np.minimum(crunchiness, flavour)      # synergy: crunch + flavor
    + 0.10 * (10 - np.abs(saltiness - 5))          # best when salt is moderate
    + noise()
)

def clip(arr):
    return np.clip(arr, 1.0, 10.0).round(2)

df = pd.DataFrame({
    "starch_pct":     starch_pct.round(3),
    "fat_pct":        fat_pct.round(3),
    "salt_pct":       salt_pct.round(3),
    "moisture_pct":   moisture_pct.round(3),
    "seasoning_pct":  seasoning_pct.round(3),
    "crunchiness":    clip(crunchiness),
    "oiliness":       clip(oiliness),
    "saltiness":      clip(saltiness),
    "flavour":        clip(flavour),
    "flavor_balance": clip(flavor_balance),
})

df.to_csv("backend/data/snacks.csv", index=False)
print(f"Snacks dataset generated: {len(df)} rows")
print(df.head())
print(df.describe().round(2))