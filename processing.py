"""Processing helpers: cleaning text and computing sentiment using vaderSentiment."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re

analyzer = SentimentIntensityAnalyzer()

def clean_text(s):
    if not isinstance(s, str):
        return ''
    s = re.sub(r'http\S+', '', s)   # remove urls
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def add_tweet_sentiment(df, text_col='text', out_col='sentiment'):
    df = df.copy()
    df[text_col] = df[text_col].fillna('').apply(clean_text)
    scores = df[text_col].apply(lambda t: analyzer.polarity_scores(t)['compound'])
    df[out_col] = scores
    return df

def aggregate_player_sentiment(tweets_df):
    """Given tweets with a 'player' column and 'sentiment', compute aggregated metrics."""
    df = tweets_df.copy()
    if 'sentiment' not in df.columns:
        df = add_tweet_sentiment(df)
    agg = df.groupby('player').agg(
        tweet_count = ('sentiment', 'count'),
        avg_sentiment = ('sentiment', 'mean'),
        max_sentiment = ('sentiment', 'max'),
        min_sentiment = ('sentiment', 'min')
    ).reset_index()
    return agg
