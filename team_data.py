"""
team_data.py
------------
Primary colours and badge URLs for Premier League and La Liga clubs.
Badge URLs point to Wikimedia Commons — no API key required.
"""

TEAM_DATA = {

    # ── Premier League (E0) ───────────────────────────────────────────────────
    "Arsenal":          {"color": "#EF0107", "badge": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"},
    "Aston Villa":      {"color": "#670E36", "badge": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg"},
    "Bournemouth":      {"color": "#DA291C", "badge": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg"},
    "Brentford":        {"color": "#E30613", "badge": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg"},
    "Brighton":         {"color": "#0057B8", "badge": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg"},
    "Burnley":          {"color": "#6C1D45", "badge": "https://upload.wikimedia.org/wikipedia/en/6/62/Burnley_F.C._Logo.svg"},
    "Cardiff":          {"color": "#0070B5", "badge": "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg"},
    "Chelsea":          {"color": "#034694", "badge": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"},
    "Crystal Palace":   {"color": "#1B458F", "badge": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg"},
    "Everton":          {"color": "#003399", "badge": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg"},
    "Fulham":           {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg"},
    "Huddersfield":     {"color": "#0E63AD", "badge": "https://upload.wikimedia.org/wikipedia/en/5/5a/Huddersfield_Town_A.F.C._logo.svg"},
    "Ipswich":          {"color": "#3A64A3", "badge": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg"},
    "Leeds":            {"color": "#1D428A", "badge": "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg"},
    "Leicester":        {"color": "#003090", "badge": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg"},
    "Liverpool":        {"color": "#C8102E", "badge": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"},
    "Luton":            {"color": "#F78F1E", "badge": "https://upload.wikimedia.org/wikipedia/en/9/9d/Luton_Town_logo.svg"},
    "Man City":         {"color": "#6CABDD", "badge": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"},
    "Man United":       {"color": "#DA291C", "badge": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"},
    "Newcastle":        {"color": "#241F20", "badge": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg"},
    "Nott'm Forest":    {"color": "#DD0000", "badge": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg"},
    "Norwich":          {"color": "#00A650", "badge": "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg"},
    "Sheffield United": {"color": "#EE2737", "badge": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg"},
    "Southampton":      {"color": "#D71920", "badge": "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"},
    "Tottenham":        {"color": "#132257", "badge": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"},
    "Watford":          {"color": "#FBEE23", "badge": "https://upload.wikimedia.org/wikipedia/en/e/e2/Watford.svg"},
    "West Brom":        {"color": "#122F67", "badge": "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg"},
    "West Ham":         {"color": "#7A263A", "badge": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg"},
    "Wolves":           {"color": "#FDB913", "badge": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg"},

    # ── La Liga (SP1) ─────────────────────────────────────────────────────────
    "Almeria":          {"color": "#CE1126", "badge": "https://upload.wikimedia.org/wikipedia/en/4/45/UD_Almería_logo_%282019%29.svg"},
    "Ath Bilbao":       {"color": "#EE2523", "badge": "https://upload.wikimedia.org/wikipedia/en/9/98/Club_Athletic_de_Bilbao_logo.svg"},
    "Ath Madrid":       {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_de_Madrid_2017_logo.svg"},
    "Barcelona":        {"color": "#A50044", "badge": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg"},
    "Betis":            {"color": "#00833E", "badge": "https://upload.wikimedia.org/wikipedia/en/1/13/Real_betis_logo.svg"},
    "Cadiz":            {"color": "#F5D000", "badge": "https://upload.wikimedia.org/wikipedia/en/5/58/Cádiz_CF_logo.svg"},
    "Celta":            {"color": "#79BADE", "badge": "https://upload.wikimedia.org/wikipedia/en/3/38/RC_Celta_de_Vigo_logo.svg"},
    "Deportivo":        {"color": "#1A3E7C", "badge": "https://upload.wikimedia.org/wikipedia/en/1/10/RC_Deportivo_de_La_Coru%C3%B1a_logo.svg"},
    "Eibar":            {"color": "#005CA9", "badge": "https://upload.wikimedia.org/wikipedia/en/8/8c/SD_Eibar_logo.svg"},
    "Elche":            {"color": "#007A33", "badge": "https://upload.wikimedia.org/wikipedia/en/0/06/Elche_CF_logo.svg"},
    "Espanol":          {"color": "#005CA9", "badge": "https://upload.wikimedia.org/wikipedia/en/4/48/RCD_Espanyol_logo.svg"},
    "Getafe":           {"color": "#005CA9", "badge": "https://upload.wikimedia.org/wikipedia/en/3/35/Getafe_CF_logo.svg"},
    "Girona":           {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/6/6b/Girona_FC_logo.svg"},
    "Granada":          {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/3/34/Granada_CF.svg"},
    "Las Palmas":       {"color": "#F5D000", "badge": "https://upload.wikimedia.org/wikipedia/en/7/76/UD_Las_Palmas_logo.svg"},
    "Leganes":          {"color": "#003DA5", "badge": "https://upload.wikimedia.org/wikipedia/en/0/04/CD_Legan%C3%A9s_logo.svg"},
    "Levante":          {"color": "#004A97", "badge": "https://upload.wikimedia.org/wikipedia/en/7/7b/Levante_UD_logo.svg"},
    "Mallorca":         {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/b/b4/RCD_Mallorca_logo.svg"},
    "Osasuna":          {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/0/00/Club_Atlético_Osasuna.svg"},
    "Rayo Vallecano":   {"color": "#CC0000", "badge": "https://upload.wikimedia.org/wikipedia/en/d/d7/Rayo_Vallecano_logo.svg"},
    "Real Madrid":      {"color": "#00529F", "badge": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"},
    "Sevilla":          {"color": "#D91A21", "badge": "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg"},
    "Sociedad":         {"color": "#003DA5", "badge": "https://upload.wikimedia.org/wikipedia/en/f/f1/Real_Sociedad_logo.svg"},
    "Valencia":         {"color": "#EE7203", "badge": "https://upload.wikimedia.org/wikipedia/en/c/ce/Valenciacf.svg"},
    "Valladolid":       {"color": "#6A0DAD", "badge": "https://upload.wikimedia.org/wikipedia/en/0/0f/Real_Valladolid_logo.svg"},
    "Villarreal":       {"color": "#F5D000", "badge": "https://upload.wikimedia.org/wikipedia/en/b/b9/Villarreal_CF_logo-en.svg"},
}


def get_team(name: str) -> dict:
    """Return color and badge for a team, with a safe fallback."""
    return TEAM_DATA.get(name, {"color": "#444444", "badge": ""})