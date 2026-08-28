"""
data/sources/football_data_api.py
----------------------------------
Fetches current season results from football-data.org API
and saves them as a CSV in the same format as football-data.co.uk CSVs.

Run directly to update:
    python -m data.sources.football_data_api --league E0
"""

import os
import argparse
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

RAW_DIR = Path(__file__).parents[1] / "raw"

# League code → API competition code
COMPETITION = {
    "E0": "PL",
    "E1": "ELC",
    "SP1": "PD",
    "D1": "BL1",
    "I1": "SA",
    "F1": "FL1",
}

# API team name → model team name (same as fixtures.py)
NAME_MAP = {
    "Arsenal FC":                  "Arsenal",
    "Aston Villa FC":              "Aston Villa",
    "AFC Bournemouth":             "Bournemouth",
    "Brentford FC":                "Brentford",
    "Brighton & Hove Albion FC":   "Brighton",
    "Burnley FC":                  "Burnley",
    "Cardiff City FC":             "Cardiff",
    "Chelsea FC":                  "Chelsea",
    "Crystal Palace FC":           "Crystal Palace",
    "Everton FC":                  "Everton",
    "Fulham FC":                   "Fulham",
    "Huddersfield Town AFC":       "Huddersfield",
    "Ipswich Town FC":             "Ipswich",
    "Leeds United FC":             "Leeds",
    "Leicester City FC":           "Leicester",
    "Liverpool FC":                "Liverpool",
    "Luton Town FC":               "Luton",
    "Manchester City FC":          "Man City",
    "Manchester United FC":        "Man United",
    "Newcastle United FC":         "Newcastle",
    "Nottingham Forest FC":        "Nott'm Forest",
    "Norwich City FC":             "Norwich",
    "Sheffield United FC":         "Sheffield United",
    "Southampton FC":              "Southampton",
    "Tottenham Hotspur FC":        "Tottenham",
    "Watford FC":                  "Watford",
    "West Bromwich Albion FC":     "West Brom",
    "West Ham United FC":          "West Ham",
    "Wolverhampton Wanderers FC":  "Wolves",
    "Coventry City FC":            "Coventry",
    "Sunderland AFC":              "Sunderland",
    "Hull City AFC":               "Hull",
    "Middlesbrough FC":            "Middlesbrough",
    "Millwall FC":                 "Millwall",
    "Oxford United FC":            "Oxford",
    "Plymouth Argyle FC":          "Plymouth",
    "Portsmouth FC":               "Portsmouth",
    "Preston North End FC":        "Preston",
    "Queens Park Rangers FC":      "QPR",
    "Sheffield Wednesday FC":      "Sheffield Weds",
    "Stoke City FC":               "Stoke",
    "Swansea City AFC":            "Swansea",
    "Bristol City FC":             "Bristol City",
    "Blackburn Rovers FC":         "Blackburn",
    "Derby County FC":             "Derby",
}

RESULT_MAP = {
    "HOME_TEAM": "H",
    "AWAY_TEAM": "A",
    "DRAW":      "D",
}


def fetch_current_season(league_code: str) -> pd.DataFrame:
    """
    Fetch all FINISHED matches for the current season from the API.
    Returns a DataFrame in the same format as football-data.co.uk CSVs.
    """
    competition = COMPETITION.get(league_code)
    if not competition:
        raise ValueError(f"No API competition code for league {league_code}")

    url = f"{BASE_URL}/competitions/{competition}/matches?status=FINISHED"
    headers = {"X-Auth-Token": API_KEY}

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    matches = r.json().get("matches", [])

    if not matches:
        print(f"  No finished matches found for {league_code}")
        return pd.DataFrame()

    rows = []
    season_label = None

    for m in matches:
        home_api = m["homeTeam"]["name"]
        away_api = m["awayTeam"]["name"]
        home = NAME_MAP.get(home_api, home_api)
        away = NAME_MAP.get(away_api, away_api)

        ft = m["score"]["fullTime"]
        ht = m["score"]["halfTime"]
        winner = m["score"]["winner"]

        date_str = m["utcDate"][:10]  # YYYY-MM-DD

        if season_label is None:
            year = int(m["season"]["startDate"][:4])
            season_label = f"{str(year)[2:]}{str(year+1)[2:]}"

        rows.append({
            "Date":    date_str,
            "HomeTeam": home,
            "AwayTeam": away,
            "FTHG":    ft["home"],
            "FTAG":    ft["away"],
            "FTR":     RESULT_MAP.get(winner, ""),
            "HTHG":    ht["home"] if ht["home"] is not None else "",
            "HTAG":    ht["away"] if ht["away"] is not None else "",
            "HTR":     RESULT_MAP.get(winner, ""),  # approximate
        })

    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"])
    print(f"  Fetched {len(df)} matches for {league_code} ({season_label})")
    return df, season_label


def save_current_season(league_code: str) -> Path:
    """
    Fetch and save current season data as a CSV in data/raw/<league>/
    Returns the path to the saved file.
    """
    df, season_label = fetch_current_season(league_code)
    if df.empty:
        return None

    out_dir = RAW_DIR / league_code
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{league_code}_{season_label}.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", required=True)
    args = parser.parse_args()
    save_current_season(args.league)