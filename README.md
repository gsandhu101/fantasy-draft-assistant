# Fantasy Draft Assistant — MVP

This is a minimal, local **MVP** for a Fantasy Football Draft Assistant that showcases:
- ingest templates for Twitter + sports APIs,
- simple data processing (sentiment + cleaning),
- a ranking / recommendation function,
- a Streamlit dashboard to explore results.

## What I built (high level)
- `ingest/twitter_ingest.py` — template that uses the Twitter/X API (Tweepy) to fetch recent tweets for beat writers or player queries. Requires your `TWITTER_BEARER_TOKEN`.
- `ingest/sports_ingest.py` — template for fetching player ADP or roster/depth info from a sports API (e.g., Sleeper, Sportsdata.io). Fill in your API key.
- `sample_data/player_adp.csv` — small example ADP dataset.
- `sample_data/sample_tweets.csv` — small example tweets dataset (used for demo).
- `processing.py` — cleans tweets and computes sentiment using `vaderSentiment`.
- `ranking.py` — basic ranking algorithm combining ADP and sentiment.
- `db.py` — simple SQLite helper to persist/load DataFrames.
- `app.py` — Streamlit app (UI) to explore players, tweets, sentiment, and recommendations.

## Quick start (run locally)

1. **Clone or unzip** the project and `cd` into it:
```bash
cd fantasy_draft_assistant
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows PowerShell
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** (copy from `.env.example`) and add your API keys if you plan to use real ingestion:
```
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
SPORTS_API_KEY=your_sports_api_key_here
SQLITE_DB_PATH=./fantasy.db
```

5. **Run the Streamlit UI**:
```bash
streamlit run app.py
```

The app will use the included sample data by default so you can explore the workflow without API keys.

## Notes & Next steps
- This is a learning scaffold. Replace the ingestion templates with your live API calls and schedule regular ingestion (Airflow / cron).
- For tweet summarization you can integrate OpenAI (or other LLM) for richer paraphrases — this demo uses VADER sentiment and short summaries.
- For production: move to PostgreSQL, add an ETL pipeline, rate-limit handling for APIs, caching, and authentication.

---

Enjoy — follow the `README` inside `/ingest` files for how to plug-in your keys and run ingestion.
