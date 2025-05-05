import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add path to the file
data_path = Path("C:/Users/siles/OneDrive/Desktop/DSKTOP/SKILLS/DS/Git REPOSITORIES/Example-Work-Product/Example-Work-Product/SPRT BTTNG")
sys.path.append(str(data_path))

from MLB_Plate_Appearance_data import mlb_df as df  # Import the DataFrame

# Random batter/pitcher handedness (replace with real data if you have it)
import numpy as np
np.random.seed(42)
df["Batter Hand"] = np.random.choice(["R", "L"], size=len(df))
df["Pitcher Hand"] = np.random.choice(["R", "L"], size=len(df))

# OBP adjustment function
def adjust_obp(obp, bh, ph):
    if bh == 'R' and ph == 'L':
        return obp + 0.020
    elif bh == 'L' and ph == 'L':
        return obp - 0.020
    elif bh == 'L' and ph == 'R':
        return obp + 0.010
    else:
        return obp + 0.005

df["Adjusted OBP"] = df.apply(lambda row: round(adjust_obp(row["OBP"], row["Batter Hand"], row["Pitcher Hand"]), 3), axis=1)

# User input for odds
odds = st.sidebar.number_input("DraftKings 'No' Odds (e.g. -150)", value=-150)

# Calculate implied probability
def implied_prob(odds):
    return abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (100 + odds)

implied_no_prob = implied_prob(odds)

# Compute edge
df["Edge %"] = ((1 - df["Adjusted OBP"]) - implied_no_prob) * 100
df["Edge %"] = df["Edge %"].round(2)

# Display controls and results
st.title("MLB Live Betting Edge Calculator")
st.markdown("**Targeting 'No' bets on Plate Appearances**")

st.write(f"Implied 'No' probability: **{implied_no_prob:.1%}**")

min_edge = st.slider("Minimum Edge (%)", min_value=-10.0, max_value=20.0, value=0.0, step=0.5)

filtered_df = df[df["Edge %"] >= min_edge].sort_values("Edge %", ascending=False)

st.dataframe(filtered_df.reset_index(drop=True))
