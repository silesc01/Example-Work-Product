import streamlit as st

# --- OBP Adjustment Function ---
def adjust_obp(obp, pitcher_hand, batter_hand="R"):  # default to R batter for now
    if batter_hand == 'R' and pitcher_hand == 'L':
        return obp + 0.020
    elif batter_hand == 'L' and pitcher_hand == 'L':
        return obp - 0.020
    elif batter_hand == 'L' and pitcher_hand == 'R':
        return obp + 0.010
    else:
        return obp + 0.005

# --- Odds to Implied Probability ---
def implied_prob(odds):
    return abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (100 + odds)

# --- Kelly Criterion ---
def kelly(win_prob, odds_decimal):
    b = odds_decimal - 1
    return ((win_prob * (b + 1)) - 1) / b

# --- Streamlit Interface ---
st.title("MLB 'No' Bet Kelly Calculator")

obp = st.number_input("Enter Player OBP (e.g. 0.278)", min_value=0.0, max_value=1.0, value=0.278, step=0.001)
pitcher_hand = st.radio("Pitcher Hand", options=["L", "R"])
batter_hand = st.radio("Batter Hand", options=["R", "L"])
odds = st.number_input("DraftKings 'No' Odds", value=-150)
unit = st.number_input("Unit Size ($)", min_value=1, value=10)
kelly_cap = st.slider("Kelly Fraction Cap", 0.0, 1.0, 1.0, 0.05)

# --- Adjust OBP and Calculate ---
adj_obp = adjust_obp(obp, pitcher_hand, batter_hand)
win_prob = 1 - adj_obp
imp_prob = implied_prob(odds)
edge = win_prob - imp_prob

st.write(f"**Adjusted OBP:** {adj_obp:.3f}")
st.write(f"**Win Probability (No Hit):** {win_prob:.1%}")
st.write(f"**Implied Probability (from Odds):** {imp_prob:.1%}")
st.write(f"**Edge:** {edge * 100:.2f}%")

# --- Decision ---
if edge <= 0:
    st.error("Don’t bet — no edge.")
else:
    odds_decimal = abs(odds) / 100 + 1 if odds < 0 else 100 / odds + 1
    k_fraction = kelly(win_prob, odds_decimal)
    k_fraction = max(0, min(k_fraction, kelly_cap))
    bet_amount = round(k_fraction * unit, 2)
    st.success(f"**Recommended Bet: ${bet_amount}** ({k_fraction:.2%} of unit)")
