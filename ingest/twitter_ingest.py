"""Template: twitter_ingest.py
Uses Tweepy Client (Twitter API v2) to fetch recent tweets for a list of usernames or search queries.
Fill your TWITTER_BEARER_TOKEN in an .env file or pass it directly.

Note: this is a template — run it locally after installing `tweepy` and setting up your keys.
"""
import os
import csv
from dotenv import load_dotenv

load_dotenv()
BEARER = os.getenv('TWITTER_BEARER_TOKEN')

def fetch_tweets_for_usernames(usernames, max_results=50, save_csv='sample_data/fetched_tweets.csv'):
    if not BEARER:
        raise ValueError('Set TWITTER_BEARER_TOKEN in your .env to use live ingestion.')
    try:
        import tweepy
    except ImportError:
        raise ImportError('Install tweepy: pip install tweepy')

    client = tweepy.Client(bearer_token=BEARER, wait_on_rate_limit=True)
    rows = []
    for username in usernames:
        user = client.get_user(username=username)
        if not user.data:
            print(f"Warning: user {username} not found (skipping)")
            continue
        uid = user.data.id
        resp = client.get_users_tweets(id=uid, max_results=min(max_results,100))
        if resp.data:
            for t in resp.data:
                rows.append({
                    'player': username,
                    'author': username,
                    'created_at': t.created_at.isoformat() if t.created_at else '',
                    'text': t.text.replace('\n',' ')
                })
    # Save CSV
    keys = ['player','author','created_at','text']
    with open(save_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} tweets to {save_csv}")
    # Write last updated timestamp
    with open('sample_data/last_updated.txt', 'w') as f:
        from datetime import datetime
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    # Real NFL beat writers and news sources
    sample_users = [
        'AdamSchefter',      # ESPN
        'RapSheet',          # Ian Rapoport, NFL Network
        'FieldYates',        # ESPN
        'TomPelissero',      # NFL Network
        'MikeClayNFL',       # ESPN
        'JayGlazer',         # FOX Sports
        'MySportsUpdate',    # NFL News aggregator
        'ProFootballTalk',   # NBC Sports
        'AroundTheNFL',      # NFL Network
        'NFL',               # Official NFL
        'PFF',               # Pro Football Focus
        'Rotoworld_FB',      # Rotoworld Football
        'MatthewBerryTMR',   # Fantasy Analyst
        'EvanSilva',         # Fantasy Analyst
        'Rotounderworld',    # Fantasy Analyst
    ]
    fetch_tweets_for_usernames(sample_users)
