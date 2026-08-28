from pathlib import Path
from typing import Optional
import yaml

_YAML_PATH = Path(__file__).parent / "leagues.yaml"


def load_leagues() -> list[dict]:
    with open(_YAML_PATH) as f:
        return yaml.safe_load(f)["leagues"]


def get_league(code: str) -> dict:
    for league in load_leagues():
        if league["code"] == code:
            return league
    raise KeyError(
        f"League '{code}' not found in leagues.yaml. "
        f"Available: {[l['code'] for l in load_leagues()]}"
    )


def list_codes() -> list[str]:
    return [l["code"] for l in load_leagues()]