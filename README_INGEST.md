# Ingest README

## Twitter ingestion (high-level)
1. Apply for a Twitter/X developer account and create an app to get a Bearer Token.
2. Set TWITTER_BEARER_TOKEN in `.env`.
3. Run `python ingest/twitter_ingest.py [tier]` with your chosen user tier — it will save a CSV.

### Rate Limiting Improvements
The Twitter ingestion has been optimized to avoid cancellation due to rate limits:
- **User tiers**: `essential` (4 users), `default` (8 users), `extended` (15 users)
- **Caching**: Reduces API calls on subsequent runs
- **Batch processing**: Prevents API overwhelm
- **Custom rate limiting**: Shorter, predictable delays

Examples:
```bash
python ingest/twitter_ingest.py essential  # Fastest, minimal API usage
python ingest/twitter_ingest.py default    # Recommended balance
python ingest/twitter_ingest.py extended   # Comprehensive coverage
```

See `TWITTER_RATE_LIMITING_FIX.md` for detailed documentation.

## Sports API ingestion
1. Pick a provider (Sleeper, Sportsdata.io, FantasyData, etc).
2. Get an API key and set SPORTS_API_KEY in `.env`.
3. Update `ingest/sports_ingest.py` endpoint and mapping code. Run to save ADP/rosters.

## Scheduling ingestion
- Use cron, a simple loop, or Airflow for regular ingestion.
- Save new rows to a database via `db.py` instead of replacing CSVs.
- Consider using `essential` tier for frequent automated runs to minimize API usage.
