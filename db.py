"""Simple SQLite helper using pandas and sqlalchemy to save/load tables."""
import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv('SQLITE_DB_PATH', './fantasy.db')

def get_engine(db_path=None):
    path = db_path or DB_PATH
    engine = create_engine(f'sqlite:///{path}')
    return engine

def save_df(df, table_name, db_path=None):
    engine = get_engine(db_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Saved {len(df)} rows to {table_name} (db={engine.url})")

def load_table(table_name, db_path=None):
    engine = get_engine(db_path)
    try:
        df = pd.read_sql_table(table_name, engine)
        return df
    except Exception as e:
        print('Error loading table:', e)
        return None
