import streamlit as st
import pandas as pd

from services.universe import load_nifty500_universe
from services.market_data import fetch_history
from services.indicators import compute_metrics

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.title("Guru Scanner")
st.caption("Nifty 500 universe loader with Yahoo Finance data and scanner filters.")

batch_size = st.sidebar.slider("Universe batch size", 1, 100, 5, 1)

st.write("Loading Nifty 500 universe...")
universe = load_nifty500_universe()
st.success(f"Universe loaded: {len(universe)} stocks")

selected = universe.head(batch_size).copy()

st.subheader("Selected Universe Preview")
st.dataframe(selected, use_container_width=True, hide_index=True)

symbols = selected["yf_symbol"].tolist()
st.write("Yahoo symbols being fetched:")
st.write(symbols)

st.write("Fetching Yahoo Finance price history...")
history = fetch_history(symbols, period="6mo", interval="1d", batch_size=5)

if history.empty:
    st.error("No price history returned from Yahoo Finance.")
    st.stop()

st.success(f"History rows fetched: {len(history)}")

st.subheader("Raw History Preview")
st.dataframe(history.head(20), use_container_width=True, hide_index=True)

metrics = compute_metrics(history, selected)

if metrics.empty:
    st.warning("Metrics dataframe is empty.")
    st.stop()

st.success(f"Metrics rows created: {len(metrics)}")

st.subheader("Metrics Preview")
st.dataframe(
    metrics[[
        "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
        "rs_score", "atr_rs_raw", "dist_52w_high_pct", "volume_surge"
    ]],
    use_container_width=True,
    hide_index=True
)
