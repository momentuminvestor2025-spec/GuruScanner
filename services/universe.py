import io
import time
import pandas as pd
import requests
import streamlit as st

NIFTY_500_CSV_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/csv,application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
}

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_nifty500_universe():
    session = requests.Session()
    session.headers.update(HEADERS)

    for attempt in range(3):
        try:
            session.get("https://www.nseindia.com/", timeout=20)
            response = session.get(NIFTY_500_CSV_URL, timeout=(10, 60))
            response.raise_for_status()

            df = pd.read_csv(io.StringIO(response.text))
            df.columns = [c.strip() for c in df.columns]

            if "Symbol" in df.columns:
                df["Symbol"] = df["Symbol"].astype(str).str.strip().str.upper()

            return df

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(2)
            else:
                break

    return pd.read_csv("data/nifty500_fallback.csv")
