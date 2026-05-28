import streamlit as st
import pandas as pd

from services.universe import load_nifty500_universe
from services.market_data import fetch_history
from services.indicators import compute_metrics

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.title("Guru Scanner")
st.caption("Nifty 500 universe loader with Yahoo Finance data and scanner filters.")

st.write("Loading Nifty 500 universe...")
universe = load_nifty500_universe()
st.success(f"Universe loaded: {len(universe)} stocks")

batch_size = st.sidebar.slider("Universe batch size", 20, 200, 60, 10)
selected = universe.head(batch_size).copy()

st.write("Fetching Yahoo Finance price history...")
history = fetch_history(selected["yf_symbol"].tolist(), period="1y", interval="1d", batch_size=25)

if history.empty:
    st.error("No price history returned from Yahoo Finance.")
    st.stop()

metrics = compute_metrics(history, selected)

st.subheader("Metrics Preview")
st.dataframe(
    metrics[[
        "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
        "rs_score", "atr_rs_raw", "dist_52w_high_pct", "volume_surge"
    ]],
    use_container_width=True,
    hide_index=True
)

st.subheader("Quick Stats")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Universe Loaded", len(selected))
c2.metric("Visible Rows", len(metrics))
c3.metric("Data Source", "Nifty CSV + Yahoo")
c4.metric("Active View", "Dashboard")
