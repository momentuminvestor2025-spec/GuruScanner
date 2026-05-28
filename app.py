import os
import pandas as pd
import streamlit as st

from components.styles import inject_global_styles, render_hero, section_header, sidebar_brand
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
from services.liquidity import apply_liquidity_filters, get_default_liquidity_profile

st.set_page_config(page_title="Guru Scanner", layout="wide")
inject_global_styles()

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
    sidebar_brand()
    st.markdown("<div class='mini-note'>Configure universe, liquidity, and sector filters.</div>", unsafe_allow_html=True)

    universe_mode = st.selectbox(
        "Universe",
        options=["Nifty 500", "Nifty 750 (Total Market)"],
        index=0
    )

    strict_liquidity = st.checkbox(
        "Strict liquidity mode",
        value=(universe_mode == "Nifty 750 (Total Market)")
    )
    enable_liquidity = st.checkbox("Enable liquidity filters", value=True)

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

defaults = get_default_liquidity_profile(universe_mode, strict_liquidity)

with st.sidebar:
    min_price = st.number_input("Min Price", min_value=1.0, value=float(defaults["min_price"]), step=5.0)
    min_avg_volume_20 = st.number_input("Min 20D Avg Volume", min_value=0, value=int(defaults["min_avg_volume_20"]), step=50000)
    min_avg_traded_value_20 = st.number_input("Min 20D Avg Traded Value", min_value=0, value=int(defaults["min_avg_traded_value_20"]), step=10000000)

metrics_liquid, metrics_before_liquidity, metrics_after_liquidity = apply_liquidity_filters(
    metrics_df=metrics,
    min_price=min_price,
    min_avg_volume_20=min_avg_volume_20,
    min_avg_traded_value_20=min_avg_traded_value_20,
    enable_filter=enable_liquidity,
)

all_sectors = sorted([s for s in metrics_liquid["sector"].dropna().unique().tolist()])

with st.sidebar:
    search_text = st.text_input("Search symbol or company")
    selected_sectors = st.multiselect("Sector", options=all_sectors, default=[])

filtered_metrics = apply_table_filters(metrics_liquid, search_text, selected_sectors)

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

leaders = filtered_metrics.sort_values(["rs_score", "dist_52w_high_pct"], ascending=[False, True]).head(12)
unknown_count = int((filtered_metrics["company"] == "Unknown Company").sum())

render_hero(universe_mode)

section_header(
    "Dashboard",
    "Market Overview",
    "Track source coverage, universe filtering, liquidity pruning, and scanner hit rates."
)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Universe Constituents", len(selected_universe), border=True)
k2.metric("Source NSE Rows", source_rows, border=True)
k3.metric("Universe Rows Used", universe_rows_used, border=True)
k4.metric("Pre-Liquidity Rows", metrics_before_liquidity, border=True)
k5.metric("Post-Liquidity Rows", metrics_after_liquidity, border=True)

a1, a2, a3, a4 = st.columns(4)
a1.metric("Q Matches", len(q_screen), border=True)
a2.metric("M Matches", len(m_screen), border=True)
a3.metric("Consensus", len(c_screen), border=True)
a4.metric("Unknown Mappings", unknown_count, border=True)

left, right = st.columns([2.1, 1])

with left:
    section_header(
        "Breadth",
        "Sector Strength",
        "Most represented sectors by surviving liquid names, ranked with average RS."
    )
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

with right:
    section_header(
        "Controls",
        "Liquidity Rules",
        "Current execution-quality guardrails applied before scanners run."
    )
    st.write(f"**Min Price:** {
