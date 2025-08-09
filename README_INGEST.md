# Ingest README

## Twitter ingestion (high-level)
1. Apply for a Twitter/X developer account and create an app to get a Bearer Token.
2. Set TWITTER_BEARER_TOKEN in `.env`.
3. Run `python ingest/twitter_ingest.py` with your chosen usernames — it will save a CSV.

## Sports API ingestion
1. Pick a provider (Sleeper, Sportsdata.io, FantasyData, etc).
2. Get an API key and set SPORTS_API_KEY in `.env`.
3. Update `ingest/sports_ingest.py` endpoint and mapping code. Run to save ADP/rosters.

## Scheduling ingestion
- Use cron, a simple loop, or Airflow for regular ingestion.
- Save new rows to a database via `db.py` instead of replacing CSVs.
