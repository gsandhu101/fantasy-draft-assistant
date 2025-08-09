# Fantasy Draft Assistant — Local Setup & Usage Instructions

This guide explains **exactly** how to run the MVP Fantasy Football Draft Assistant locally.

---

## 1. Prerequisites

Before running this app, make sure you have:

- **Python 3.9+** installed (`python --version` to check).
- **pip** (Python package manager).
- **Virtual environment support** (`python -m venv`).
- **GitHub Copilot** or any IDE for editing.

Optional (for live data ingestion):
- Twitter/X Developer Account & **Bearer Token**.
- Sports data API key (e.g., Sportsdata.io, Sleeper API, etc.).

---

## 2. Download / Clone Project

If you have the `.zip` file:
```bash
# Replace with the actual path to your downloaded zip
unzip fantasy_draft_assistant.zip
cd fantasy_draft_assistant
```

If using GitHub:
```bash
git clone https://github.com/yourusername/fantasy_draft_assistant.git
cd fantasy_draft_assistant
```

---

## 3. Create Virtual Environment

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows PowerShell:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

You should now see `(venv)` in your terminal prompt.

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run With Sample Data (No API Keys Needed)

This app comes with **sample ADP data** and **sample tweets** so you can see it in action immediately.

```bash
streamlit run app.py
```

- Your browser should open automatically to `http://localhost:8501`.
- Use the sidebar to explore player data, tweets, and draft recommendations.

---

## 6. Configure Live Data (Optional, Advanced)

If you want **live tweets** and **real ADP**:

1. Copy `.env.example` → `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and fill in:
   ```env
   TWITTER_BEARER_TOKEN=your_twitter_token_here
   SPORTS_API_KEY=your_sports_api_key_here
   SQLITE_DB_PATH=./fantasy.db
   ```

3. **Run Twitter ingestion**:
   ```bash
   python ingest/twitter_ingest.py
   ```
   This will save fetched tweets to `sample_data/fetched_tweets.csv`.

4. **Run sports API ingestion**:
   ```bash
   python ingest/sports_ingest.py
   ```
   This will save updated ADP to `sample_data/adp_live.csv`.

5. Update `app.py` to load your live CSVs instead of sample data.

---

## 7. How It Works (MVP Workflow)

1. **Ingestion**: Fetch tweets & player data from APIs.
2. **Processing**: Clean text & calculate sentiment using `vaderSentiment`.
3. **Ranking**: Combine Average Draft Position (ADP) + sentiment into a draft score.
4. **UI**: Streamlit dashboard for easy exploration.

---

## 8. Next Steps for Learning

- Replace CSV ingestion with **database persistence** (`db.py` is ready for SQLite/PostgreSQL).
- Add **scheduling** with cron or Airflow to pull fresh data regularly.
- Use **OpenAI API** to summarize tweets into actionable player notes.
- Improve ranking algorithm with injuries, matchups, and positional scarcity.

---

## 9. Troubleshooting

- **Port 8501 in use** → Stop other Streamlit apps or run:  
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Module not found** → Make sure you're in the virtual environment and ran `pip install -r requirements.txt`.

---

## 10. License

MIT License — use, modify, and share freely.
