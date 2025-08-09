"""Streamlit UI for exploring sample data and seeing recommendations."""
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

from processing import add_tweet_sentiment, aggregate_player_sentiment
from ranking import compute_rankings

st.set_page_config(page_title='Fantasy Draft Assistant MVP', layout='wide')

st.title('Fantasy Draft Assistant — MVP')

DATA_DIR = 'sample_data'
adp_path = os.path.join(DATA_DIR, 'player_adp.csv')
tweets_path = os.path.join(DATA_DIR, 'sample_tweets.csv')
adp_live_path = os.path.join(DATA_DIR, 'adp_live.csv')
tweets_live_path = os.path.join(DATA_DIR, 'fetched_tweets.csv')
last_updated_path = os.path.join(DATA_DIR, 'last_updated.txt')

def get_last_updated():
    if os.path.exists(last_updated_path):
        with open(last_updated_path, 'r') as f:
            return f.read().strip()
    return 'Never'

st.sidebar.header('Controls')
sample_mode = st.sidebar.selectbox('Data mode', ['Sample (included)', 'Live (use APIs)'])
max_tweets = st.sidebar.slider('Max tweets shown per player', 1, 20, 5)

# Display last updated timestamp at top right
st.markdown(f"<div style='text-align:right; font-size:0.9em;'>Last updated: {get_last_updated()}</div>", unsafe_allow_html=True)

@st.cache_data
def load_data(mode):
    # Try to load live data if available
    if mode == 'Live (use APIs)':
        adp = pd.read_csv(adp_live_path) if os.path.exists(adp_live_path) else pd.read_csv(adp_path)
        tweets = pd.read_csv(tweets_live_path) if os.path.exists(tweets_live_path) else pd.read_csv(tweets_path)
    else:
        adp = pd.read_csv(adp_path)
        tweets = pd.read_csv(tweets_path)
    return adp, tweets

adp, tweets = load_data(sample_mode)

st.header(f"Player ADP ({'live' if sample_mode == 'Live (use APIs)' else 'sample'})")
st.dataframe(adp)

st.header(f"Recent Tweets ({'live' if sample_mode == 'Live (use APIs)' else 'sample'})")
player_select = st.selectbox('Show tweets for player', ['All'] + sorted(tweets['player'].unique().tolist()))
if player_select == 'All':
    display_tweets = tweets
else:
    display_tweets = tweets[tweets['player'] == player_select].head(max_tweets)
display_tweets = add_tweet_sentiment(display_tweets)
st.dataframe(display_tweets[['player','author','created_at','text','sentiment']])

st.header('Recommendations (combined ADP + sentiment)')
sent_agg = aggregate_player_sentiment(display_tweets) if player_select != 'All' else aggregate_player_sentiment(tweets)
rankings = compute_rankings(adp, sent_agg)
st.dataframe(rankings[['rank','player','position','team','adp','tweet_count','avg_sentiment','draft_score']])

st.markdown('---')
st.subheader('Notes')
st.markdown('''- This is an MVP to learn and extend. Replace `sample_data` ingestion with live API ingestion scripts in `/ingest`.
- Tweak weights in `ranking.py` to match your draft strategy (value RBs early, prefer high-volume WRs, etc).
- To add live tweeting: run `ingest/twitter_ingest.py`, save tweets into `sample_data/fetched_tweets.csv`, then modify `app.py` to load live file.
''')
