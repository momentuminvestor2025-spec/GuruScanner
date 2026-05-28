import os
import pandas as pd
import streamlit as st

from services.universe import load_nifty500_universe
from services.universe_filters import filter_to_nifty500_universe
from services.indicators import compute_metrics
from services.scanners import (
    run_qullamaggie_screen,
    run_minervini_screen,
    run_consensus_screen,
)
from services.filters import apply_table_filters
from services.export_utils import dataframe_to_csv_bytes

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.markdown("""
<style>
div[data-testid="metric-container"] {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    padding: 10px 14px;
    border-radius: 14px;
}
div[data-testid="metric-container"] label {
    color: #64748b !important;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Guru Scanner")
st.caption("Cache-first scanner mode — Nifty 500 filtered from full NSE source")

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

history_n500, source_rows, nifty500_rows = filter_to_nifty500_universe(history, universe)

if history_n500.empty:
    st.error("No Nifty 500 rows found in latest_prices.csv after filtering.")
    st.stop()

metrics = compute_metrics(history_n500, universe)

if metrics.empty:
    st.warning("Metrics dataframe is empty after Nifty 500 filtering.")
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

top_sectors = (
    filtered_metrics.groupby("sector", dropna=False)
    .agg(
        stocks=("symbol", "count"),
        avg_rs=("rs_score", "mean")
    )
    .sort_values(["stocks", "avg_rs"], ascending=[False, False])
    .reset_index()
    .head(10)
)

unknown_count = int((filtered_metrics["company"] == "Unknown Company").sum())

st.markdown("### Dashboard")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Universe", len(universe), border=True)
k2.metric("Source NSE Rows", source_rows, border=True)
k3.metric("Nifty500 Rows Used", nifty500_rows, border=True)
k4.metric("Q Matches", len(filtered_q), border=True)
k5.metric("Consensus", len(filtered_c), border=True)

a1, a2, a3 = st.columns(3)
a1.metric("Metrics Rows", len(filtered_metrics), border=True)
a2.metric("M Matches", len(filtered_m), border=True)
a3.metric("Unknown Mappings", unknown_count, border=True)

summary_left, summary_right = st.columns([2, 1])

with summary_left:
    st.subheader("Sector Strength")
    if top_sectors.empty:
        st.info("No sector summary available.")
    else:
        st.dataframe(
            top_sectors.round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "avg_rs": st.column_config.NumberColumn("Average RS", format="%.2f")
            }
        )

with summary_right:
    st.subheader("Export")
    st.download_button(
        label="Download Qullamaggie CSV",
        data=dataframe_to_csv_bytes(filtered_q),
        file_name="qullamaggie_scanner.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label="Download Minervini CSV",
        data=dataframe_to_csv_bytes(filtered_m),
        file_name="minervini_scanner.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label="Download Consensus CSV",
        data=dataframe_to_csv_bytes(filtered_c),
        file_name="consensus_scanner.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label="Download Metrics CSV",
        data=dataframe_to_csv_bytes(filtered_metrics),
        file_name="metrics_preview.csv",
        mime="text/csv",
        use_container_width=True
    )

tabs = st.tabs([
    "Qullamaggie",
    "Minervini",
    "Consensus",
    "Metrics Preview",
    "Filtered Price Preview",
])

scanner_cols = [
    "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
    "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
    "volume_surge", "badge"
]

with tabs[0]:
    st.subheader("Qullamaggie Scanner")
    if filtered_q.empty:
        st.info("No Qullamaggie matches yet.")
    else:
        st.dataframe(filtered_q[scanner_cols].round(2), use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Minervini Scanner")
    if filtered_m.empty:
        st.info("No Minervini matches yet.")
    else:
        st.dataframe(filtered_m[scanner_cols].round(2), use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("Consensus Scanner")
    if filtered_c.empty:
        st.info("No overlap names yet.")
    else:
        st.dataframe(filtered_c.round(2), use_container_width=True, hide_index=True)

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
    st.dataframe(filtered_metrics[metrics_cols].round(2), use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Filtered Price Preview")
    st.dataframe(history_n500.head(100), use_container_width=True, hide_index=True)
