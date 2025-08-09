"""Simple ranking algorithm that combines ADP (lower is better) with sentiment (higher is better).
This produces a single 'draft_score' where higher is better.
"""
import pandas as pd
import numpy as np

def compute_rankings(adp_df, sentiment_agg_df, adp_col='adp'):
    # Merge ADP with sentiment
    df = pd.merge(adp_df, sentiment_agg_df, how='left', left_on='player', right_on='player')
    df['tweet_count'] = df['tweet_count'].fillna(0)
    df['avg_sentiment'] = df['avg_sentiment'].fillna(0)

    # Normalize ADP into a score where higher is better
    # We invert adp so that lower ADP -> higher value
    df['adp_norm'] = df[adp_col].rank(ascending=False, method='min') / df[adp_col].rank(ascending=False).max()
    # sentiment is already roughly -1..1 from VADER; shift to 0..1
    df['sentiment_norm'] = (df['avg_sentiment'] + 1) / 2

    # Simple linear combination: weights can be tuned
    df['draft_score'] = 0.7 * df['adp_norm'] + 0.3 * df['sentiment_norm']

    df = df.sort_values('draft_score', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
    return df
