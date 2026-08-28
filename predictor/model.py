import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor, XGBClassifier

# Constants
MODELS_DIR = Path(__file__).parents[1]/'models'
FEATURE_COLS = [
    'Home_Form_Points_last5', 'Home_Form_GF_last5', 'Home_Form_GA_last5',
    'Home_Form_SoT_F_last5', 'Home_Form_CleanSheet_last5', 'Home_DaysSinceLast',
    'Away_Form_Points_last5', 'Away_Form_GF_last5', 'Away_Form_GA_last5',
    'Away_Form_SoT_F_last5', 'Away_Form_CleanSheet_last5', 'Away_DaysSinceLast',
    'Home_AttackStrength', 'Home_DefenceStrength',
    'Away_AttackStrength', 'Away_DefenceStrength',
    'H2H_HomeWins', 'H2H_Draws', 'H2H_AwayWins', 'H2H_Meetings',
    'MatchNum', 'HomeAdvantage'
]
MAX_GOALS = 8

class FootballPredictor:

    def __init__(self, league_code):
        self.league_code = league_code
        self._clf = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('clf', XGBClassifier(random_state=42, n_jobs=-1))
        ])
        self._reg_h = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('clf', XGBRegressor(random_state=42, n_jobs=-1))
        ])
        self._reg_a = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('clf', XGBRegressor(random_state=42, n_jobs=-1))
        ])
        self._le = LabelEncoder()
        self.trained = False

    def fit (self, features):

        df = features.dropna(subset = ['Result']).copy()

        X = df[FEATURE_COLS]
        Y = self._le.fit_transform(df['Result'])

        self._clf.fit(X, Y)
        self._reg_h.fit(X, df['FTHG'])
        self._reg_a.fit(X, df['FTAG'])
        self.trained = True

        return self

    def predict(self, match_features):
        if(self.trained == False):
            raise RuntimeError("Model is not trained")

        X = match_features[FEATURE_COLS]
        clf_probs = self._clf.predict_proba(X)
        xg_home = np.clip(self._reg_h.predict(X), 0.1, MAX_GOALS)
        xg_away = np.clip(self._reg_a.predict(X), 0.1, MAX_GOALS)

        results = []

        for i in range(len(match_features)):
            home_probs = np.array([poisson.pmf(g, xg_home[i]) for g in range(MAX_GOALS + 1)])
            away_probs = np.array([poisson.pmf(g, xg_away[i])for g in range(MAX_GOALS + 1)])
            matrix = np.outer(home_probs, away_probs)

            p_home = float(np.tril(matrix, -1).sum())
            p_draw = float(np.trace(matrix))
            p_away = float(np.triu(matrix, 1).sum())

            label_order = list(self._le.classes_)
            clf_map = {label_order[j]: clf_probs[i, j] for j in range(3)}

            blended_h = 0.6 * clf_map.get('H', 0) + 0.4 * p_home
            blended_a = 0.6 * clf_map.get('A', 0) + 0.4 * p_away
            blended_d = 0.6 * clf_map.get('D', 0) + 0.4 * p_draw

            idx = np.unravel_index(np.argmax(matrix), matrix.shape)

            results.append({
                'prob_home_win': round(blended_h, 4),
                'prob_draw':     round(blended_d, 4),
                'prob_away_win': round(blended_a, 4),
                'xg_home':       round(float(xg_home[i]), 2),
                'xg_away':       round(float(xg_away[i]), 2),
                'score_home':    int(idx[0]),
                'score_away':    int(idx[1]),
            })

        return results

    def save(self, models_dir=MODELS_DIR):
        models_dir.mkdir(parents=True, exist_ok=True)
        path = models_dir / f'{self.league_code}_model.pkl'
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        print(path)
        return path
    
    @classmethod
    def load(cls, league_code, models_dir = MODELS_DIR):
        path = models_dir / f'{league_code}_model.pkl'
        if not path.exists():
            raise FileNotFoundError()
        with open(path, 'rb') as f:
            return pickle.load(f)
             

