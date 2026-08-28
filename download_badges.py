"""
download_badges.py
------------------
Downloads club badges from ESPN's CDN and saves them to badges/
Run once: python download_badges.py
"""

import requests
from pathlib import Path

BADGES_DIR = Path("badges")
BADGES_DIR.mkdir(exist_ok=True)

# ESPN team IDs
TEAM_IDS = {
"Aston Villa":      58,
"Ath Madrid":       1068,
"Betis":            1069,
"Espanol":          1072,
"Girona":           9812,
"Granada":          9813,
"Las Palmas":       1077,
"Leganes":          9818,
"Levante":          1079,
"Mallorca":         1080,
"Osasuna":          1081,
"Rayo Vallecano":   9835,
"Sevilla":          1082,
"Sociedad":         1084,
"Valencia":         1086,
"Valladolid":       9843,
"Villarreal":       1087,
}

BASE_URL = "https://a.espncdn.com/i/teamlogos/soccer/500/{id}.png"
headers = {"User-Agent": "Mozilla/5.0"}

print("script started")
print(f"Downloading {len(TEAM_IDS)} badges...\n")
ok, failed = 0, []

for team, team_id in TEAM_IDS.items():
    filename = team.replace(" ", "_").replace("'", "") + ".png"
    path = BADGES_DIR / filename
    if path.exists():
        print(f"  ⏭  {team} (cached)")
        ok += 1
        continue
    url = BASE_URL.format(id=team_id)
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and len(r.content) > 500:
            path.write_bytes(r.content)
            print(f"  ✅ {team}")
            ok += 1
        else:
            print(f"  ❌ {team} — HTTP {r.status_code}")
            failed.append(team)
    except Exception as e:
        print(f"  ❌ {team} — {e}")
        failed.append(team)

print(f"\nDone: {ok} downloaded, {len(failed)} failed.")
if failed:
    print("Failed:", failed)