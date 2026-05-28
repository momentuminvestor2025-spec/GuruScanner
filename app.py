import os
import pandas as pd
import streamlit as st

from services.universe import load_nifty500_universe
from services.indicators import compute_metrics
from services.scanners import (
    run_qullamaggie_screen,
    run_minervini_screen,
    run_consensus_screen,
)
from services.filters import apply_table_filters

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

universe = load_nifty500_universe()
metrics = compute_metrics(history, universe)

if metrics.empty:
    st.warning("Metrics dataframe is empty.")
    st.stop()

q_screen = run_qullamaggie_screen(metrics)
m_screen = run_minervini_screen(metrics)
c_screen = run_consensus_screen(q_screen, m_screen)

all_sectors = sorted([s for s in metrics["sector"].dropna().unique().tolist()])

with st.sidebar:
    st.header("Filters")
    search_text = st.text_input("Search symbol or company")
    selected_sectors = st.multiselect("Sector", options=all_sectors, default=[])

filtered_metrics = apply_table_filters(metrics, search_text, selected_sectors)
filtered_q = apply_table_filters(q_screen, search_text, selected_sectors)
filtered_m = apply_table_filters(m_screen, search_text, selected_sectors)
filtered_c = apply_table_filters(c_screen, search_text, selected_sectors)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Universe", len(universe), border=True)
k2.metric("Price Rows", len(history), border=True)
k3.metric("Q Matches", len(filtered_q), border=True)
k4.metric("M Matches", len(filtered_m), border=True)
k5.metric("Consensus", len(filtered_c), border=True)

tabs = st.tabs([
    "Qullamaggie",
    "Minervini",
    "Consensus",
    "Metrics Preview",
    "Raw Price Preview",
])

scanner_cols = [
    "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
    "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
    "volume_surge", "badge"
]

with tabs[0]:
    st.subheader("Qullamaggie Scanner")
    if filtered_q.empty:
        st.info("No Qullamaggie matches yet. Add more historical rows and more symbols to latest_prices.csv.")
    else:
        st.dataframe(
            filtered_q[scanner_cols].round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "daily_pct": st.column_config.NumberColumn("Daily %", format="%.2f"),
                "weekly_pct": st.column_config.NumberColumn("Weekly %", format="%.2f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.1f"),
                "atr_rs": st.column_config.NumberColumn("ATR RS", format="%.1f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "range_pos_20": st.column_config.NumberColumn("20D Range %", format="%.2f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

with tabs[1]:
    st.subheader("Minervini Scanner")
    if filtered_m.empty:
        st.info("No Minervini matches yet. This is normal with very small sample history.")
    else:
        st.dataframe(
            filtered_m[scanner_cols].round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "daily_pct": st.column_config.NumberColumn("Daily %", format="%.2f"),
                "weekly_pct": st.column_config.NumberColumn("Weekly %", format="%.2f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.1f"),
                "atr_rs": st.column_config.NumberColumn("ATR RS", format="%.1f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "range_pos_20": st.column_config.NumberColumn("20D Range %", format="%.2f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

with tabs[2]:
    st.subheader("Consensus Scanner")
    if filtered_c.empty:
        st.info("No overlap names yet. Consensus will populate after at least one stock appears in both scanners.")
    else:
        st.dataframe(
            filtered_c.round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "daily_pct": st.column_config.NumberColumn("Daily %", format="%.2f"),
                "weekly_pct": st.column_config.NumberColumn("Weekly %", format="%.2f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.1f"),
                "atr_rs": st.column_config.NumberColumn("ATR RS", format="%.1f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "range_pos_20": st.column_config.NumberColumn("20D Range %", format="%.2f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

with tabs[3]:
    st.subheader("Metrics Preview")
    metrics_cols = [
        "symbol", "company", "sector", "close",
        "ema10", "sma20", "sma50", "sma100", "sma200",
        "daily_pct", "weekly_pct",
        "rs_score", "atr_rs",
        "dist_52w_high_pct", "range_pos_20",
        "volume_surge", "ma_aligned", "green_day", "near_high"
    ]
    st.dataframe(
        filtered_metrics[metrics_cols].round(2),
        use_container_width=True,
        hide_index=True
    )

with tabs[4]:
    st.subheader("Raw Price Preview")
    st.dataframe(history.head(100), use_container_width=True, hide_index=True)
