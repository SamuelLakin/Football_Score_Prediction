import numpy as np
import pandas as pd
import typing

FORM_WINDOW = 5 #number of recent matches for form
H2H_WINDOW = 5 #past head-to-head meetings
MIN_MATCHES = 3 #min matches before stats maeningful

#convert match results to points
def _result_points(result, perspective):
    if result == 'D':
        return 1
    elif (result == 'A' and perspective == 'away') or (result == 'H' and perspective == 'home'):
        return 3
    else:
        return 0

def _build_team_match_log(df: pd.DataFrame):
    home = df[['Date', 'Season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HST', 'AST']].copy()
    home.columns = ['Date', 'Season', 'Team', 'Opponent', 'GF', 'GA', 'FTR', 'SoT_F', 'SoT_A']

    home['Venue'] = 'home' 
    home['Points'] = home.apply(lambda row: _result_points(row['FTR'], 'home'), axis=1)

    away = df[['Date', 'Season', 'AwayTeam', 'HomeTeam', 'FTAG', 'FTHG', 'FTR', 'AST', 'HST']].copy()
    away.columns = ['Date', 'Season', 'Team', 'Opponent', 'GF', 'GA', 'FTR', 'SoT_F', 'SoT_A']

    away['Venue'] = 'away'
    away['Points'] = away.apply(lambda row: _result_points(row['FTR'], 'away'), axis=1)

    df_final: pd.DataFrame = pd.concat([home, away], ignore_index=True)
    df_final = df_final.sort_values(by=['Date'])

    df_final['CleanSheet'] = (df_final['GA'] == 0).astype(int)

    return df_final


def _rolling_team_stats(log: pd.DataFrame, window = FORM_WINDOW):
    stats_cols = ['Points', 'GF', 'GA', 'SoT_F', 'CleanSheet']
    log = log.sort_values(['Team', 'Date']).reset_index(drop = True)

    rolled = (
        log.groupby('Team')[stats_cols]
        .apply(lambda g: g.shift(1).rolling(window, min_periods=1).mean())
        .reset_index(level=0, drop=True)
    )

    log['DaysSinceLast'] = log.groupby('Team')['Date'].diff().dt.days.fillna(7)
    rolled.columns = [f'Form_{c}_last{window}'for c in stats_cols] 

    df_res: pd.DataFrame = pd.concat([log[['Date', 'Team', 'Venue', 'DaysSinceLast']], rolled], axis=1)

    return df_res

def _season_strength(df: pd.DataFrame):
    records = []

    for season, sdf in df.groupby('Season'):
        sdf = sdf.sort_values('Date').reset_index(drop=True)

        lg_avg_home = sdf['FTHG'].expanding().mean().shift(1).fillna(sdf['FTHG'].mean())
        lg_avg_away = sdf['FTAG'].expanding().mean().shift(1).fillna(sdf['FTAG'].mean())

        for idx, row in sdf.iterrows():
            date = row['Date']
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            past = sdf[sdf['Date'] < date]

            for team, venue in [(home_team, 'home'), (away_team, 'away')]:
                team_home = past[past['HomeTeam'] == team]
                team_away = past[past['AwayTeam'] == team]

                goals_scored = pd.concat([team_home['FTHG'], team_away['FTAG']])
                goals_conceded = pd.concat([team_home['FTAG'], team_away['FTHG']])

                n = len(goals_scored)
                avg_scored = goals_scored.mean() if n > 0 else lg_avg_home.iloc[idx]
                avg_conceded = goals_conceded.mean() if n > 0 else lg_avg_away.iloc[idx]
                lg_avg = lg_avg_home.iloc[idx] if venue == 'home' else lg_avg_away.iloc[idx]

                att = avg_scored / lg_avg if lg_avg > 0 else 1.0
                def_ = avg_conceded / lg_avg if lg_avg > 0 else 1.0

                records.append({
                    'Date' : date, 'Season' : season, 'Team' : team,
                    'Venue': venue, 'AttackStrength': att, 'DefenceStrength': def_
                })
    return pd.DataFrame(records)

def _h2h_features(df: pd.DataFrame, window = H2H_WINDOW):

    df = df.sort_values('Date')
    records = []
    for idx, row in df.iterrows():

        date = row['Date']
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']

        past: pd.DataFrame = df[
            (df['Date'] < date) &
            (
            ((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team)) |
            ((df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team))
            )
        ].tail(window)

        h2h_home_wins = 0
        h2h_draws = 0
        h2h_away_wins = 0

        for _, row in past.iterrows():
            if row['HomeTeam'] == home_team:
                if row['FTR'] == 'H': h2h_home_wins +=1
                elif row['FTR'] == 'D' : h2h_draws += 1
                else: h2h_away_wins +=1
            else:
                if row['FTR'] == 'A': h2h_away_wins +=1
                elif row['FTR'] == 'D': h2h_draws +=1
                else: h2h_home_wins +=1

        records.append({'idx': idx, 'H2H_HomeWins': h2h_home_wins, 'H2H_Draws': h2h_draws, 'H2H_AwayWins': h2h_away_wins, 'H2H_Meetings': len(past)})

    return records

def build_features(raw: pd.DataFrame):
    print('Building team match log...')
    log = _build_team_match_log(raw)
    print('Computing rolling form...')
    rolling =_rolling_team_stats(log)
    print('Computing season-level attach/defence strenghts...')
    strengths = _season_strength(raw)
    print('Computing head-to-head features...')
    h2h = _h2h_features(raw)

    home_roll = rolling[rolling['Venue'] == 'home'].set_index(['Date', 'Team'])
    away_roll = rolling[rolling['Venue'] == 'away'].set_index(['Date', 'Team'])

    home_roll.columns = ['Home_' + c if c not in ('Date', 'Team', 'Venue') else c for c in home_roll.columns]
    away_roll.columns = ['Away_' + c if c not in ('Date', 'Team', 'Venue') else c for c in away_roll.columns]

    home_str = strengths[strengths['Venue'] == 'home'].set_index(['Date', 'Team'])
    away_str = strengths[strengths['Venue'] == 'away'].set_index(['Date', 'Team'])

    home_str = home_str[['AttackStrength', 'DefenceStrength']]
    away_str = away_str[['AttackStrength', 'DefenceStrength']]

    home_str.columns = ['Home_'  + c if c not in ('Date', 'Team', 'Venue') else c for c in home_str.columns]
    away_str.columns = ['Away_'  + c if c not in ('Date', 'Team', 'Venue') else c for c in away_str.columns]

    feat = raw[['Date', 'Season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].copy()
    feat = feat.rename(columns={'FTR': 'Result'})

    feat = feat.join(home_roll, on=['Date', 'HomeTeam'])
    #feat = feat.join(away_roll, on=['Date', 'AwayTeam'])
    feat = feat.join(away_roll.drop(columns=['Venue']), on=['Date', 'AwayTeam'])
    feat = feat.join(home_str, on=['Date', 'HomeTeam'])
    feat = feat.join(away_str, on = ['Date', 'AwayTeam'])
    feat = feat.join(pd.DataFrame(h2h))

    feat['MatchNum'] = feat.groupby('Season').cumcount() + 1
    feat['HomeAdvantage'] = 1
    feat = feat.dropna(subset=['Result']).reset_index(drop=True)

    return feat

