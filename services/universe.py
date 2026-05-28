import io
import time
import pandas as pd
import requests
import streamlit as st

NIFTY_500_CSV_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
NIFTY_TOTAL_MARKET_CSV_URL = "https://niftyindices.com/IndexConstituent/ind_niftytotalmarket_list.csv"

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

def _standardize_universe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        "Company Name": "company",
        "Industry": "sector",
        "Symbol": "symbol",
        "Company Name (Full Name)": "company",
        "Company Name (Company Name)": "company",
    }
    df = df.rename(columns=rename_map)

    if "symbol" not in df.columns:
        raise ValueError("symbol column not found in universe file")

    if "company" not in df.columns:
        df["company"] = df["symbol"]

    if "sector" not in df.columns:
        df["sector"] = "Unknown"

    df["symbol"] = df["symbol"].astype(str).map(_normalize_symbol)
    df["company"] = df["company"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()
    df["yf_symbol"] = df["symbol"] + ".NS"

    return df[["symbol", "company", "sector", "yf_symbol"]].drop_duplicates()

def _download_csv(url: str) -> pd.DataFrame:
    session = requests.Session()
    session.headers.update(HEADERS)

    for attempt in range(3):
        try:
            session.get("https://www.nseindia.com/", timeout=20)
            response = session.get(url, timeout=(10, 60))
            response.raise_for_status()
            return pd.read_csv(io.StringIO(response.text))
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(2)
            else:
                raise

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_nifty500_universe():
    try:
        df = _download_csv(NIFTY_500_CSV_URL)
        return _standardize_universe(df)
    except Exception:
        fallback = pd.read_csv("data/nifty500_fallback.csv")
        return _standardize_universe(fallback)

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_nifty750_universe():
    try:
        df = _download_csv(NIFTY_TOTAL_MARKET_CSV_URL)
        return _standardize_universe(df)
    except Exception:
        fallback_500 = pd.read_csv("data/nifty500_fallback.csv")
        fallback_micro = pd.read_csv("data/niftymicro250_fallback.csv")
        combined = pd.concat([fallback_500, fallback_micro], ignore_index=True).drop_duplicates()
        return _standardize_universe(combined)

def load_selected_universe(universe_mode: str) -> pd.DataFrame:
    if universe_mode == "Nifty 750 (Total Market)":
        return load_nifty750_universe()
    return load_nifty500_universe()
