import argparse
import sys
from pathlib import Path
import pandas as pd
from config import load_leagues, get_league, list_codes
from data.downloader import fetch
from features.engineer import build_features
from predictor.model import FootballPredictor
from datetime import datetime


PROCESSED_DIR = Path(__file__).parent/ 'data' / 'processed'

def run_league(league_code, start_year = None, end_year= None, force = False):
    print(f'Running pipeline for {league_code}...')

    raw = fetch(
        league_code=league_code,
        start_year=start_year,
        end_year = end_year or datetime.now().year,
        force=force
    )

    features = build_features(raw)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    feat_path = PROCESSED_DIR / f'{league_code}_features.parquet'
    features.to_parquet(feat_path, index=False)
    print(f'Features saved -> {feat_path.name}')

    model = FootballPredictor(league_code=league_code)
    model.fit(features)
    model.save()

    return features, model

def main():
    parser = argparse.ArgumentParser(description='Football Predictor Pipeline')
    parser.add_argument("--league", nargs='+', metavar='CODE')
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--force", action='store_true')

    args = parser.parse_args()

    for code in args.league:
        run_league(league_code=code,
                   start_year=args.start, 
                   end_year=args.end,
                   force=args.force)
if __name__ == '__main__':
    main()