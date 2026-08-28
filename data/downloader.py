from pathlib import Path
import pandas as pd

from config import get_league
from data.sources.football_data import fetch_league as _fetch_football_data

RAW_DIR = Path(__file__).parent / "raw"

_ADAPTERS = {
    "football_data": _fetch_football_data,
}


def fetch(
    league_code: str,
    start_year: int | None = None,
    end_year:   int | None = None,
    raw_dir:    Path = RAW_DIR,
    force:      bool = False,
) -> pd.DataFrame:
    cfg = get_league(league_code)

    start = start_year or cfg["start_year"]
    end   = end_year   or 2024

    source  = cfg.get("source", "football_data")
    adapter = _ADAPTERS.get(source)

    if adapter is None:
        raise ValueError(f"No adapter registered for source '{source}'.")

    print(f"\n[{cfg['name']}] Fetching {start}–{end} via '{source}' …")
    return adapter(
        league_code=league_code,
        start_year=start,
        end_year=end,
        raw_dir=raw_dir,
        force=force,
    )