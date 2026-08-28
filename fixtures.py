"""
fixtures.py
-----------
Fetches upcoming fixtures from football-data.org API.
Maps API team names to the names used in the model.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

# API competition codes
LEAGUE_TO_COMPETITION = {
    "E0": "PL",   # Premier League
    "E1": "ELC",  # Championship
    "SP1": "PD",  # La Liga
    "D1": "BL1",  # Bundesliga
    "I1": "SA",   # Serie A
    "F1": "FL1",  # Ligue 1
}

# Map API full names → model short names
NAME_MAP = {
    # Premier League
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

    # Championship
    "Blackburn Rovers FC":         "Blackburn",
    "Bristol City FC":             "Bristol City",
    "Burnley FC":                  "Burnley",
    "Cardiff City FC":             "Cardiff",
    "Coventry City FC":            "Coventry",
    "Derby County FC":             "Derby",
    "Hull City AFC":               "Hull",
    "Leeds United FC":             "Leeds",
    "Luton Town FC":               "Luton",
    "Middlesbrough FC":            "Middlesbrough",
    "Millwall FC":                 "Millwall",
    "Norwich City FC":             "Norwich",
    "Oxford United FC":            "Oxford",
    "Plymouth Argyle FC":          "Plymouth",
    "Portsmouth FC":               "Portsmouth",
    "Preston North End FC":        "Preston",
    "Queens Park Rangers FC":      "QPR",
    "Sheffield Wednesday FC":      "Sheffield Weds",
    "Stoke City FC":               "Stoke",
    "Sunderland AFC":              "Sunderland",
    "Swansea City AFC":            "Swansea",
    "Watford FC":                  "Watford",
    "West Bromwich Albion FC":     "West Brom",

    # La Liga
    "UD Almería":                  "Almeria",
    "Athletic Club":               "Ath Bilbao",
    "Atlético de Madrid":          "Ath Madrid",
    "FC Barcelona":                "Barcelona",
    "Real Betis Balompié":         "Betis",
    "Cádiz CF":                    "Cadiz",
    "RC Celta de Vigo":            "Celta",
    "RCD Espanyol de Barcelona":   "Espanol",
    "Getafe CF":                   "Getafe",
    "Girona FC":                   "Girona",
    "Granada CF":                  "Granada",
    "UD Las Palmas":               "Las Palmas",
    "CD Leganés":                  "Leganes",
    "Levante UD":                  "Levante",
    "RCD Mallorca":                "Mallorca",
    "CA Osasuna":                  "Osasuna",
    "Rayo Vallecano de Madrid":    "Rayo Vallecano",
    "Real Madrid CF":              "Real Madrid",
    "Sevilla FC":                  "Sevilla",
    "Real Sociedad de Fútbol":     "Sociedad",
    "Valencia CF":                 "Valencia",
    "Real Valladolid CF":          "Valladolid",
    "Villarreal CF":               "Villarreal",
}


def get_upcoming_fixtures(league_code: str) -> list[dict]:
    """
    Returns a list of upcoming fixtures for the given league code.
    Each fixture is a dict with: home, away, date.
    Returns [] if the league isn't supported or the API call fails.
    """
    competition = LEAGUE_TO_COMPETITION.get(league_code)
    if not competition:
        return []

    url = f"{BASE_URL}/competitions/{competition}/matches?status=SCHEDULED&limit=20"
    headers = {"X-Auth-Token": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return []
        matches = r.json().get("matches", [])
    except Exception:
        return []

    fixtures = []
    for m in matches:
        home_api = m["homeTeam"]["name"]
        away_api = m["awayTeam"]["name"]
        home = NAME_MAP.get(home_api, home_api)
        away = NAME_MAP.get(away_api, away_api)
        date = m["utcDate"][:10]
        fixtures.append({"home": home, "away": away, "date": date})

    return fixtures