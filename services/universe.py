import io
import time
import pandas as pd
import requests
import streamlit as st

NIFTY_500_CSV_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/csv,application/json,text/plain,*/*",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
}

def _normalize_symbol(value: str) -> str:
    if pd.isna(value):
        return ""
    return (
        str(value)
        .strip()
        .upper()
        .replace("&", "")
        .replace("-", "")
        .replace(" ", "")
    )

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

            rename_map = {
                "Company Name": "company",
                "Industry": "sector",
                "Symbol": "symbol",
            }
            df = df.rename(columns=rename_map)

            if "symbol" not in df.columns:
                raise ValueError("symbol column not found in Nifty 500 universe file")

            if "company" not in df.columns:
                df["company"] = df["symbol"]

            if "sector" not in df.columns:
                df["sector"] = "Unknown"

            df["symbol"] = df["symbol"].astype(str).map(_normalize_symbol)
            df["company"] = df["company"].astype(str).str.strip()
            df["sector"] = df["sector"].astype(str).str.strip()
            df["yf_symbol"] = df["symbol"] + ".NS"

            return df[["symbol", "company", "sector", "yf_symbol"]].drop_duplicates()

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(2)
            else:
                break

    fallback = pd.read_csv("data/nifty500_fallback.csv")
    fallback["symbol"] = fallback["symbol"].astype(str).map(_normalize_symbol)
    fallback["company"] = fallback["company"].astype(str).str.strip()
    fallback["sector"] = fallback["sector"].astype(str).str.strip()
    fallback["yf_symbol"] = fallback["symbol"] + ".NS"
    return fallback[["symbol", "company", "sector", "yf_symbol"]].drop_duplicates()
