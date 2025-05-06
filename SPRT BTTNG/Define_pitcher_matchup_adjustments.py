# Define pitcher matchup adjustments for OBP
# We'll create approximate OBP adjustments for typical platoon splits
def adjust_obp_for_matchup(obp, batter_hand, pitcher_hand):
    if batter_hand == 'R' and pitcher_hand == 'L':
        return obp + 0.020  # RHB vs LHP gets bump
    elif batter_hand == 'L' and pitcher_hand == 'L':
        return obp - 0.020  # LHB vs LHP gets penalty
    elif batter_hand == 'L' and pitcher_hand == 'R':
        return obp + 0.010  # LHB vs RHP small bump
    else:
        return obp + 0.005  # RHB vs RHP very small bump

# For simplicity, randomly assign batter and pitcher handedness
import numpy as np
np.random.seed(42)  # reproducibility
df_combined['Batter Hand'] = np.random.choice(['R', 'L'], size=len(df_combined))
df_combined['Pitcher Hand'] = np.random.choice(['R', 'L'], size=len(df_combined))

# Apply the OBP adjustment
df_combined['Adjusted OBP'] = df_combined.apply(
    lambda row: round(adjust_obp_for_matchup(row['OBP'], row['Batter Hand'], row['Pitcher Hand']), 3),
    axis=1
)

import ace_tools as tools; tools.display_dataframe_to_user(name="OBP Data with Pitcher Hand Adjustments", dataframe=df_combined)
