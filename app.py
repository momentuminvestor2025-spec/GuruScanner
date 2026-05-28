import os
import pandas as pd
import streamlit as st

from services.universe import load_selected_universe
from services.universe_filters import filter_to_selected_universe
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

with st.sidebar:
    st.header("Filters")
    universe_mode = st.selectbox(
        "Universe",
        options=["Nifty 500", "Nifty 750 (Total Market)"],
        index=0
    )

selected_universe = load_selected_universe(universe_mode)

history_filtered, source_rows, universe_rows_used = filter_to_selected_universe(
    history,
    selected_universe
)

if history_filtered.empty:
    st.error(f"No rows found in latest_prices.csv for {universe_mode}.")
    st.stop()

metrics = compute_metrics(history_filtered, selected_universe)

if metrics.empty:
    st.warning(f"Metrics dataframe is empty for {universe_mode}.")
    st.stop()

all_sectors = sorted([s for s in metrics["sector"].dropna().unique().tolist()])

with st.sidebar:
    search_text = st.text_input("Search symbol or company")
    selected_sectors = st.multiselect("Sector", options=all_sectors, default=[])

filtered_metrics = apply_table_filters(metrics, search_text, selected_sectors)

q_screen = run_qullamaggie_screen(filtered_metrics)
m_screen = run_minervini_screen(filtered_metrics)
c_screen = run_consensus_screen(q_screen, m_screen)

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

st.caption(f"Cache-first scanner mode — {universe_mode} filtered from full NSE source")
st.markdown("### Dashboard")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Universe Constituents", len(selected_universe), border=True)
k2.metric("Source NSE Rows", source_rows, border=True)
k3.metric("Universe Rows Used", universe_rows_used, border=True)
k4.metric("Q Matches", len(q_screen), border=True)
k5.metric("Consensus", len(c_screen), border=True)

a1, a2, a3 = st.columns(3)
a1.metric("Metrics Rows", len(filtered_metrics), border=True)
a2.metric("M Matches", len(m_screen), border=True)
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
        label=f"Download Qullamaggie CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(q_screen),
        file_name=f"qullamaggie_{universe_mode.lower().replace(' ', '_').replace('(', '').replace(')', '')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Minervini CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(m_screen),
        file_name=f"minervini_{universe_mode.lower().replace(' ', '_').replace('(', '').replace(')', '')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Consensus CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(c_screen),
        file_name=f"consensus_{universe_mode.lower().replace(' ', '_').replace('(', '').replace(')', '')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Metrics CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(filtered_metrics),
        file_name=f"metrics_{universe_mode.lower().replace(' ', '_').replace('(', '').replace(')', '')}.csv",
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
    st.subheader(f"Qullamaggie Scanner — {universe_mode}")
    if q_screen.empty:
        st.info("No Qullamaggie matches yet.")
    else:
        st.dataframe(q_screen[scanner_cols].round(2), use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader(f"Minervini Scanner — {universe_mode}")
    if m_screen.empty:
        st.info("No Minervini matches yet.")
    else:
        st.dataframe(m_screen[scanner_cols].round(2), use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader(f"Consensus Scanner — {universe_mode}")
    if c_screen.empty:
        st.info("No overlap names yet.")
    else:
        st.dataframe(c_screen.round(2), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader(f"Metrics Preview — {universe_mode}")
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
    st.subheader(f"Filtered Price Preview — {universe_mode}")
    st.dataframe(history_filtered.head(100), use_container_width=True, hide_index=True)
