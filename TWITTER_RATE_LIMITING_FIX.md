# Twitter Ingestion Rate Limiting Fix

## Problem
The original Twitter ingestion script was getting cancelled due to excessive rate limiting:
- Processing 15 users sequentially
- 2 API calls per user (get_user + get_users_tweets) = 30 total calls
- `wait_on_rate_limit=True` caused 15+ minute sleeps when hitting limits
- Operations were cancelled in CI/CD environments due to timeouts

## Solution Overview
The improved implementation reduces API calls and provides better rate limiting control:

### Key Improvements
1. **Reduced API Calls**: User list tiering (4-15 users) + caching reduces total calls
2. **Batch Processing**: Process users in smaller batches with delays
3. **User ID Caching**: Eliminates repeated `get_user` calls on subsequent runs
4. **Custom Rate Limiting**: Shorter, predictable delays instead of 15+ minute waits
5. **Graceful Error Handling**: Partial success, retries, comprehensive logging
6. **Configurable Behavior**: Easy customization of timing and user lists

### API Call Reduction
- **Essential tier**: 4 users = 73% fewer API calls
- **Default tier**: 8 users = 47% fewer API calls  
- **With caching**: Subsequent runs only need 1 API call per user (no user lookup)

## Usage

### Basic Usage (Backward Compatible)
```bash
python ingest/twitter_ingest.py
```
Uses the default tier (8 high-value accounts).

### Tier-Based Usage
```bash
# Minimal API usage - only critical breaking news (4 accounts)
python ingest/twitter_ingest.py essential

# Balanced approach - essential + fantasy analysts (8 accounts) 
python ingest/twitter_ingest.py default

# Comprehensive coverage - all accounts (15 accounts)
python ingest/twitter_ingest.py extended
```

### User Tiers
- **Essential** (4 users): AdamSchefter, RapSheet, FieldYates, TomPelissero
- **Default** (8 users): Essential + MikeClayNFL, MatthewBerryTMR, EvanSilva, PFF
- **Extended** (15 users): All original accounts for comprehensive coverage

## Configuration

### Rate Limiting Settings (`ingest/twitter_config.py`)
```python
BATCH_SIZE = 5              # Users per batch
DELAY_BETWEEN_BATCHES = 30  # Seconds between batches  
DELAY_BETWEEN_USERS = 2     # Seconds between individual users
MAX_RETRIES = 3             # Retry attempts for failed requests
RETRY_DELAY = 60            # Seconds before retrying
```

### Caching Settings
```python
CACHE_ENABLED = True                    # Enable user ID caching
CACHE_FILE = 'sample_data/user_cache.json'  # Cache file location
```

### API Settings
```python
MAX_TWEETS_PER_USER = 50               # Tweets to fetch per user
USE_CUSTOM_RATE_LIMITING = True        # Use custom vs tweepy built-in rate limiting
```

## Expected Behavior

### First Run (No Cache)
- **Essential tier**: ~2 minutes total (4 users × 2 calls + delays)
- **Default tier**: ~3 minutes total (8 users, 1 batch delay)
- **Extended tier**: ~6 minutes total (15 users, 2 batch delays)

### Subsequent Runs (With Cache)
- **Essential tier**: ~1 minute total (4 users × 1 call + delays)
- **Default tier**: ~2 minutes total (8 users, 1 batch delay)
- **Extended tier**: ~4 minutes total (15 users, 2 batch delays)

### Rate Limit Handling
- Custom delays: 60 seconds between retries (vs 15+ minutes)
- Batch delays: 30 seconds between groups of 5 users
- User delays: 2 seconds between individual users
- Maximum 3 retry attempts per user

## Logging
The script provides comprehensive logging:
```
2025-08-24 22:36:45,047 - INFO - Starting Twitter ingestion with 'default' tier (8 users)...
2025-08-24 22:36:45,048 - INFO - Users: ['AdamSchefter', 'RapSheet', ...]
2025-08-24 22:36:45,126 - INFO - Processing batch 1: ['AdamSchefter', 'RapSheet', ...]
2025-08-24 22:36:45,126 - INFO - Using cached user ID for AdamSchefter: 79298
2025-08-24 22:36:45,129 - INFO - Fetched 47 tweets for AdamSchefter
```

## Migration from Original Script
The new script is backward compatible. Existing calls to `fetch_tweets_for_usernames()` will work unchanged, but will benefit from the improved rate limiting and error handling.

For scheduled jobs, consider:
1. Start with `essential` tier to minimize API usage
2. Use `default` tier for balanced coverage
3. Only use `extended` tier if you have high API limits
4. Monitor logs to ensure stable operation

## Troubleshooting

### If Still Getting Rate Limited
1. Reduce tier: `extended` → `default` → `essential`
2. Increase delays in `twitter_config.py`:
   ```python
   DELAY_BETWEEN_BATCHES = 60  # Increase from 30
   DELAY_BETWEEN_USERS = 5     # Increase from 2
   ```
3. Reduce batch size:
   ```python
   BATCH_SIZE = 3  # Reduce from 5
   ```

### If Getting Cancelled
1. Check CI/CD timeout settings (should allow 5-10 minutes)
2. Use `essential` tier for fastest completion
3. Consider running less frequently (every 2-4 hours vs hourly)

### Cache Issues
- Cache file: `sample_data/user_cache.json`
- Delete cache file to force fresh user lookups
- Disable caching: Set `CACHE_ENABLED = False` in config

## Files Modified
- `ingest/twitter_ingest.py` - Main ingestion script with improved rate limiting
- `ingest/twitter_config.py` - Configuration and user list management