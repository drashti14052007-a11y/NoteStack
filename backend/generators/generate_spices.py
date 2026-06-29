import pandas as pd
import numpy as np

np.random.seed(13)
n = 1000

# --- INGREDIENT RANGES ---
chili_pct    = np.random.uniform(0.0,  40.0, n)   # red chili %
cumin_pct    = np.random.uniform(0.0,  30.0, n)   # cumin %
coriander_pct= np.random.uniform(0.0,  30.0, n)   # coriander %
turmeric_pct = np.random.uniform(0.0,  15.0, n)   # turmeric %
salt_pct     = np.random.uniform(0.0,  10.0, n)   # salt %

noise = lambda: np.random.normal(0, 0.3, n)

# --- SENSORY EQUATIONS ---

# Pungency: chili is dominant; fat in cumin oil slightly moderates it
# interaction term: cumin slightly amplifies chili heat
pungency = (
    (chili_pct / 40) * 8 + 1           # maps 0%→1, 40%→9
    + 0.03 * chili_pct * (cumin_pct / 30)   # interaction: cumin amplifies chili
    + noise()
)

# Aroma: cumin + coriander are the aroma drivers
aroma = (
    (cumin_pct / 30) * 4               # cumin contributes up to 4 points
    + (coriander_pct / 30) * 4         # coriander contributes up to 4 points
    + 1                                 # base
    + noise()
)

# Colour intensity: turmeric is the primary colorant in Indian spice blends
colour = (
    (turmeric_pct / 15) * 8 + 1        # maps 0%→1, 15%→9
    + 0.02 * chili_pct                 # chili adds red colour
    + noise()
)

# Saltiness: direct
saltiness = (
    (salt_pct / 10) * 8 + 1            # maps 0%→1, 10%→9
    + noise()
)

# Overall liking: balance is key — too much chili hurts
overall_liking = (
    0.20 * aroma
    + 0.15 * colour
    + 0.20 * saltiness
    + 0.20 * (10 - pungency)           # very high pungency reduces liking
    + 0.25 * pungency * 0.4            # but some heat is liked
    + noise()
)

def clip(arr):
    return np.clip(arr, 1.0, 10.0).round(2)

df = pd.DataFrame({
    "chili_pct":       chili_pct.round(3),
    "cumin_pct":       cumin_pct.round(3),
    "coriander_pct":   coriander_pct.round(3),
    "turmeric_pct":    turmeric_pct.round(3),
    "salt_pct":        salt_pct.round(3),
    "pungency":        clip(pungency),
    "aroma":           clip(aroma),
    "colour":          clip(colour),
    "saltiness":       clip(saltiness),
    "overall_liking":  clip(overall_liking),
})

df.to_csv("backend/data/spices.csv", index=False)
print(f"Spices dataset generated: {len(df)} rows")
print(df.head())
print(df.describe().round(2))