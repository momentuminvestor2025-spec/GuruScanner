import os
import pandas as pd
import streamlit as st

from services.universe import load_nifty500_universe
from services.indicators import compute_metrics
from services.scanners import run_qullamaggie_screen

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.title("Guru Scanner")
st.caption("Cache-first scanner mode")

price_file = "data/latest_prices.csv"

if not os.path.exists(price_file):
    st.error("No cached price file found. Please generate latest_prices.csv first.")
    st.stop()

if os.path.getsize(price_file) == 0:
    st.error("latest_prices.csv exists but is empty. Please regenerate the file with data.")
    st.stop()

try:
    history = pd.read_csv(price_file)
except pd.errors.EmptyDataError:
    st.error("latest_prices.csv has no valid CSV content. Please regenerate it.")
    st.stop()

st.success(f"Loaded cached price history: {len(history)} rows")

universe = load_nifty500_universe()
st.success(f"Universe loaded: {len(universe)} stocks")

metrics = compute_metrics(history, universe)

if metrics.empty:
    st.warning("Metrics dataframe is empty.")
    st.stop()

q_screen = run_qullamaggie_screen(metrics)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Universe Rows", f"{len(universe)}")
c2.metric("Price Rows", f"{len(history)}")
c3.metric("Metrics Rows", f"{len(metrics)}")
c4.metric("Qullamaggie Matches", f"{len(q_screen)}")

tab1, tab2, tab3 = st.tabs(["Qullamaggie", "Metrics Preview", "Raw Price Preview"])

with tab1:
    st.subheader("Qullamaggie Scanner")
    if q_screen.empty:
        st.info("No Qullamaggie matches yet. Add more historical rows and more symbols to latest_prices.csv.")
    else:
        display_cols = [
            "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
            "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
            "volume_surge", "badge"
        ]
        st.dataframe(
            q_screen[display_cols].round(2),
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.subheader("Metrics Preview")
    preview_cols = [
        "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
        "ema10", "sma20", "sma50", "sma100", "sma200",
        "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
        "volume_surge", "ma_aligned"
    ]
    st.dataframe(
        metrics[preview_cols].round(2),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("Raw Price Preview")
    st.dataframe(history.head(50), use_container_width=True, hide_index=True)
