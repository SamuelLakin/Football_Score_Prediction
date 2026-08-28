import base64
import streamlit as st
import pandas as pd
from pathlib import Path
from predictor.model import FootballPredictor
from config import list_codes, get_league
from team_data import get_team
from fixtures import get_upcoming_fixtures

st.set_page_config(layout="wide", page_title="Football Predictor")

st.markdown("""
<style>
    .panel {
        border-radius: 12px;
        padding: 24px;
        min-height: 500px;
    }
    .team-name {
        font-size: 2em;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
        margin-bottom: 16px;
    }
    .stat-box {
        background: rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 12px;
        margin-top: 16px;
        color: white;
    }
    .stat-label {
        font-size: 0.8em;
        opacity: 0.85;
    }
    .stat-value {
        font-size: 1.4em;
        font-weight: bold;
    }
    .center-panel {
        text-align: center;
        padding: 24px 12px;
    }
    .score-box {
        font-size: 3em;
        font-weight: bold;
        margin: 20px 0;
    }
    .league-label {
        font-size: 0.9em;
        color: #888;
        margin-bottom: 8px;
    }
    .draw-box {
        background: #f0f0f0;
        border-radius: 8px;
        padding: 12px;
        margin-top: 16px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)


def badge_path(team_name: str) -> Path:
    filename = team_name.replace(" ", "_").replace("'", "") + ".png"
    return Path("badges") / filename


def badge_b64(team_name: str) -> str:
    bp = badge_path(team_name)
    if bp.exists():
        data = bp.read_bytes()
        b64 = base64.b64encode(data).decode()
        return f"data:image/png;base64,{b64}"
    return ""


def show_prediction(result, home_team, away_team, league_code):
    home_color = get_team(home_team)["color"]
    away_color = get_team(away_team)["color"]
    home_img = badge_b64(home_team)
    away_img = badge_b64(away_team)

    home_badge_html = f'<img src="{home_img}" width="70" style="margin-bottom:12px;display:block;"><br>' if home_img else ""
    away_badge_html = f'<img src="{away_img}" width="70" style="margin-bottom:12px;display:block;"><br>' if away_img else ""

    left, centre, right = st.columns([2, 1, 2])

    with left:
        st.markdown(f"""
        <div class="panel" style="background:{home_color};">
            {home_badge_html}
            <div class="team-name">{home_team}</div>
            <div class="stat-box">
                <div class="stat-label">Win probability</div>
                <div class="stat-value">{result['prob_home_win']*100:.1f}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Expected goals</div>
                <div class="stat-value">{result['xg_home']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with centre:
        league_name = get_league(league_code)["name"]
        st.markdown(f"""
        <div class="center-panel">
            <div class="league-label">{league_name}</div>
            <div class="score-box">{result['score_home']} – {result['score_away']}</div>
            <div class="league-label">Predicted score</div>
            <div class="draw-box">
                <div class="stat-label">Draw probability</div>
                <div class="stat-value">{result['prob_draw']*100:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="panel" style="background:{away_color};">
            {away_badge_html}
            <div class="team-name">{away_team}</div>
            <div class="stat-box">
                <div class="stat-label">Win probability</div>
                <div class="stat-value">{result['prob_away_win']*100:.1f}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Expected goals</div>
                <div class="stat-value">{result['xg_away']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚽ Match Predictor")
    codes = list_codes()
    league_code = st.selectbox("League", codes, format_func=lambda c: get_league(c)["name"])

    try:
        features = pd.read_parquet(f"data/processed/{league_code}_features.parquet")
        model = FootballPredictor.load(league_code)
        teams = sorted(features["HomeTeam"].unique())
    except FileNotFoundError:
        st.warning(f"No model found for {league_code}.\nRun: python pipeline.py --league {league_code}")
        st.stop()

    mode = st.radio("Mode", ["Upcoming Fixtures", "Pick Teams"])

    if mode == "Pick Teams":
        home_team = st.selectbox("Home Team", teams)
        away_team = st.selectbox("Away Team", [t for t in teams if t != home_team])
        predict_btn = st.button("Predict", use_container_width=True)
    else:
        predict_btn = False

# ── Main area ─────────────────────────────────────────────────────────────────
if mode == "Upcoming Fixtures":
    st.subheader("Upcoming Fixtures")
    fixtures = get_upcoming_fixtures(league_code)

    if not fixtures:
        st.info("No upcoming fixtures found for this league.")
    else:
        for fix in fixtures:
            home = fix["home"]
            away = fix["away"]
            date = fix["date"]
            label = f"{home}  vs  {away}  —  {date}"

            if home in teams and away in teams:
                if st.button(label, key=label):
                    row = features[
                        (features["HomeTeam"] == home) &
                        (features["AwayTeam"] == away)
                    ].tail(1)
                    if row.empty:
                        st.warning("No historical data for this fixture.")
                    else:
                        result = model.predict(row)[0]
                        show_prediction(result, home, away, league_code)
            else:
                pass

elif predict_btn:
    row = features[
        (features["HomeTeam"] == home_team) &
        (features["AwayTeam"] == away_team)
    ].tail(1)

    if row.empty:
        st.warning("No historical data found for this fixture.")
    else:
        result = model.predict(row)[0]
        show_prediction(result, home_team, away_team, league_code)

else:
    st.markdown("""
    <div style="text-align:center; margin-top: 100px; color: #888;">
        <h2>Select a fixture or pick two teams to predict.</h2>
    </div>
    """, unsafe_allow_html=True)