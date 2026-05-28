import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_history(symbol: str, period: str = '6mo') -> pd.DataFrame:
    ticker = yf.Ticker(f"{symbol}.NS")
    hist = ticker.history(period=period, interval='1d', auto_adjust=False)
    if hist.empty:
        return pd.DataFrame()
    hist = hist.reset_index()
    hist.columns = [str(c).lower().replace(' ', '_') for c in hist.columns]
    return hist
