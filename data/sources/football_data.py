import time
from pathlib import Path
 
import pandas as pd
import requests
 
# ── URL template ──────────────────────────────────────────────────────────────
# e.g.  https://www.football-data.co.uk/mmz4281/2324/E0.csv
BASE_URL = "https://www.football-data.co.uk/mmz4281/{season}/{code}.csv"
 
# Columns to keep (subset of what football-data.co.uk provides)
CORE_COLS = [
    "Div", "Date", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR",      # full-time goals + result
    "HTHG", "HTAG", "HTR",      # half-time
    "HS",   "AS",               # shots
    "HST",  "AST",              # shots on target
    "HC",   "AC",               # corners
    "HY",   "AY",               # yellow cards
    "HR",   "AR",               # red cards
]
 
 
# ── Helpers ───────────────────────────────────────────────────────────────────
 
def _season_code(start_year: int) -> str:
    """2023 → '2324'"""
    y1 = str(start_year)[2:]
    y2 = str(start_year + 1)[2:]
    return f"{y1}{y2}"
 
 
def _url(league_code: str, start_year: int) -> str:
    return BASE_URL.format(season=_season_code(start_year), code=league_code)
 
 
# ── Public API ────────────────────────────────────────────────────────────────
 
def download_season(
    league_code: str,
    start_year: int,
    raw_dir: Path,
    force: bool = False,
) -> Path:
    """Download one season for one league. Returns local path."""
    season = _season_code(start_year)
    dest   = raw_dir / league_code / f"{league_code}_{season}.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
 
    if dest.exists() and not force:
        print(f"  ✓ [{league_code}] {season} cached")
        return dest
 
    url  = _url(league_code, start_year)
    print(f"  ↓ [{league_code}] {season} — {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return dest
 
 
def load_season(path: Path, season_label: str, league_code: str) -> pd.DataFrame:
    """Load a raw CSV, normalise columns, add metadata."""
    df = pd.read_csv(path, encoding="latin-1", on_bad_lines='skip')
 
    keep = [c for c in CORE_COLS if c in df.columns]
    df   = df[keep].copy()
 
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"], inplace=True)
 
    df["Season"] = season_label
    df["League"] = league_code
    return df.sort_values("Date").reset_index(drop=True)
 
 
def fetch_league(
    league_code: str,
    start_year: int,
    end_year: int,
    raw_dir: Path,
    force: bool = False,
) -> pd.DataFrame:
    """
    Download and concatenate all seasons for a league.
    Returns a normalised DataFrame.
    """
    frames = []
    for year in range(start_year, end_year + 1):
        season = _season_code(year)
        try:
            path = download_season(league_code, year, raw_dir, force=force)
            df   = load_season(path, season_label=season, league_code=league_code)
            frames.append(df)
            time.sleep(0.25)
        except requests.HTTPError as e:
            print(f"  ✗ [{league_code}] {season}: {e}")
 
    if not frames:
        raise RuntimeError(f"No data fetched for league '{league_code}'.")
 
    out = pd.concat(frames, ignore_index=True).sort_values("Date")
    print(f"  ✅ [{league_code}] {len(out):,} matches loaded")
    return out