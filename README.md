# Football Match Predictor

A machine learning app that predicts football match outcomes using XGBoost and Poisson regression.

## Features
- W/D/L probabilities
- Predicted scoreline and expected goals
- Supports Premier League, La Liga, Championship and more
- Live upcoming fixtures via football-data.org API

## Screenshot
<img width="1320" height="931" alt="Screenshot 2026-08-28 at 14 36 20" src="https://github.com/user-attachments/assets/6a76697a-a4e8-4e92-a420-8168c2a644d4" />


## How it works
The model uses two heads blended 60/40:
- **XGBoost classifier** — trained on rolling form, attack/defence strength, head-to-head records and home advantage
- **Poisson regression** — predicts expected goals and derives scoreline probabilities

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API key to `.env`: `FOOTBALL_DATA_API_KEY=your_key`
5. Run the pipeline: `python pipeline.py --league E0`
6. Launch the app: `streamlit run app.py`
