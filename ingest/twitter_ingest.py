"""Template: twitter_ingest.py
Uses Tweepy Client (Twitter API v2) to fetch recent tweets for a list of usernames or search queries.
Fill your TWITTER_BEARER_TOKEN in an .env file or pass it directly.

Note: this is a template — run it locally after installing `tweepy` and setting up your keys.
"""
import os
import csv
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import configuration from the same directory
try:
    from .twitter_config import *
except ImportError:
    # Fallback for direct execution
    from twitter_config import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
BEARER = os.getenv('TWITTER_BEARER_TOKEN')

def load_user_cache():
    """Load cached user ID mappings to reduce API calls."""
    if not CACHE_ENABLED:
        return {}
        
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning(f"Could not load cache file {CACHE_FILE}, starting fresh")
    return {}

def save_user_cache(cache):
    """Save user ID mappings to cache file."""
    if not CACHE_ENABLED:
        return
        
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
        logger.info(f"Saved user cache with {len(cache)} entries")
    except IOError as e:
        logger.error(f"Failed to save cache: {e}")

def fetch_tweets_with_resilience(client, usernames, max_results=None, save_csv='sample_data/fetched_tweets.csv'):
    """
    Fetch tweets with improved resilience and rate limiting.
    
    Key improvements:
    1. User ID caching to reduce API calls
    2. Batch processing to avoid overwhelming the API
    3. Custom rate limiting with shorter delays
    4. Graceful error handling and partial success
    5. Progress tracking and logging
    """
    if max_results is None:
        max_results = MAX_TWEETS_PER_USER
        
    logger.info(f"Starting tweet fetch for {len(usernames)} users")
    
    # Load cached user IDs
    user_cache = load_user_cache()
    rows = []
    successful_users = 0
    failed_users = 0
    
    # Process users in batches
    for i in range(0, len(usernames), BATCH_SIZE):
        batch = usernames[i:i + BATCH_SIZE]
        logger.info(f"Processing batch {i//BATCH_SIZE + 1}: {batch}")
        
        for username in batch:
            success = False
            for attempt in range(MAX_RETRIES):
                try:
                    # Try to get user ID from cache first
                    user_id = user_cache.get(username)
                    
                    if user_id is None:
                        # Cache miss - fetch user data
                        logger.info(f"Fetching user data for {username} (attempt {attempt + 1})")
                        user = client.get_user(username=username)
                        if not user.data:
                            logger.warning(f"User {username} not found (skipping)")
                            failed_users += 1
                            break
                        user_id = user.data.id
                        user_cache[username] = user_id
                        logger.info(f"Cached user ID for {username}: {user_id}")
                    else:
                        logger.info(f"Using cached user ID for {username}: {user_id}")
                    
                    # Fetch tweets for this user
                    logger.info(f"Fetching tweets for {username}")
                    resp = client.get_users_tweets(id=user_id, max_results=min(max_results, 100))
                    
                    if resp.data:
                        tweet_count = 0
                        for t in resp.data:
                            rows.append({
                                'player': username,
                                'author': username,
                                'created_at': t.created_at.isoformat() if t.created_at else '',
                                'text': t.text.replace('\n', ' ')
                            })
                            tweet_count += 1
                        logger.info(f"Fetched {tweet_count} tweets for {username}")
                    else:
                        logger.warning(f"No tweets found for {username}")
                    
                    successful_users += 1
                    success = True
                    break
                    
                except Exception as e:
                    logger.error(f"Error fetching data for {username} (attempt {attempt + 1}): {e}")
                    if attempt < MAX_RETRIES - 1:
                        logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                        time.sleep(RETRY_DELAY)
                    else:
                        logger.error(f"Failed to fetch data for {username} after {MAX_RETRIES} attempts")
                        failed_users += 1
            
            # Small delay between users to be respectful to the API
            if success and DELAY_BETWEEN_USERS > 0:
                time.sleep(DELAY_BETWEEN_USERS)
        
        # Delay between batches (except for the last batch)
        if i + BATCH_SIZE < len(usernames) and DELAY_BETWEEN_BATCHES > 0:
            logger.info(f"Batch complete. Waiting {DELAY_BETWEEN_BATCHES} seconds before next batch...")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    # Save the updated cache
    save_user_cache(user_cache)
    
    # Save results
    if rows:
        keys = ['player', 'author', 'created_at', 'text']
        os.makedirs(os.path.dirname(save_csv), exist_ok=True)
        with open(save_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"Saved {len(rows)} tweets to {save_csv}")
    else:
        logger.warning("No tweets were fetched!")
    
    # Write last updated timestamp
    timestamp_file = 'sample_data/last_updated.txt'
    os.makedirs(os.path.dirname(timestamp_file), exist_ok=True)
    with open(timestamp_file, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Summary
    logger.info(f"Fetch complete: {successful_users} successful, {failed_users} failed, {len(rows)} total tweets")
    return len(rows)

def fetch_tweets_for_usernames(usernames, max_results=None, save_csv='sample_data/fetched_tweets.csv'):
    """Main function that maintains backward compatibility while using improved implementation."""
    if not BEARER:
        raise ValueError('Set TWITTER_BEARER_TOKEN in your .env to use live ingestion.')
    try:
        import tweepy
    except ImportError:
        raise ImportError('Install tweepy: pip install tweepy')

    # Create client with or without built-in rate limiting based on config
    client = tweepy.Client(bearer_token=BEARER, wait_on_rate_limit=not USE_CUSTOM_RATE_LIMITING)
    
    try:
        return fetch_tweets_with_resilience(client, usernames, max_results, save_csv)
    except Exception as e:
        logger.error(f"Fatal error in tweet fetching: {e}")
        raise

if __name__ == '__main__':
    import sys
    
    # Allow command line argument to specify user tier
    tier = 'default'
    if len(sys.argv) > 1:
        tier = sys.argv[1]
    
    try:
        users = get_user_list(tier)
        logger.info(f"Starting Twitter ingestion with '{tier}' tier ({len(users)} users)...")
        logger.info(f"Users: {users}")
        
        tweet_count = fetch_tweets_for_usernames(users)
        logger.info(f"Twitter ingestion completed successfully. Total tweets: {tweet_count}")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nUsage: python twitter_ingest.py [tier]")
        print(f"Available tiers:")
        print(f"  essential - {len(ESSENTIAL_USERS)} critical breaking news accounts")
        print(f"  default   - {len(DEFAULT_USERS)} essential + fantasy analysts (recommended)")
        print(f"  extended  - {len(ALL_USERS)} all accounts for comprehensive coverage")
        exit(1)
    except Exception as e:
        logger.error(f"Twitter ingestion failed: {e}")
        exit(1)
