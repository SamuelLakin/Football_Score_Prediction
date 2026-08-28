from predictor.model import FootballPredictor
import pandas as pd

model = FootballPredictor.load('SP1')
features = pd.read_parquet('data/processed/SP1_features.parquet')

home = 'Real Madrid'
away = 'Espanol'

row = features[(features['HomeTeam'] == home) & (features['AwayTeam'] == away)].tail(1)
result = model.predict(row)[0]

print(f"\n{home} vs {away}")
print(f"Home win: {result['prob_home_win']*100:.1f}%")
print(f"Draw:     {result['prob_draw']*100:.1f}%")
print(f"Away win: {result['prob_away_win']*100:.1f}%")
print(f"xG:       {result['xg_home']} – {result['xg_away']}")
print(f"Score:    {result['score_home']} – {result['score_away']}")