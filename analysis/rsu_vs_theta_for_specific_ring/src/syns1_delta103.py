"""
Calculate the RSU for the syn-S-1 conformation with delta=103 for different
tilting angles (theta) and save the result to a CSV file.
"""

import os

import pandas as pd

from rsuanalyzer.core.rsu import calc_rsu

CONF_ID_OF_RING = "RRFFLLBBRRFFLLBB"
THETAS = range(0, 91, 1)
DELTA_ = 103

df = pd.DataFrame({
    "theta": THETAS,
    "rsu": [calc_rsu(CONF_ID_OF_RING, theta, DELTA_) for theta in THETAS]
    })

OUTPUT_FOLDER = "analysis/rsu_vs_theta_for_specific_ring/output/"
OUTPUT_FILENAME = "syn-S-1 (delta=103).csv"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

df.to_csv(OUTPUT_FOLDER + OUTPUT_FILENAME, index=False)
print(f"Saved to {OUTPUT_FOLDER + OUTPUT_FILENAME}")