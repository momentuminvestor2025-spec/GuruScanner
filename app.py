import os
import pandas as pd
import streamlit as st

from components.styles import (
    inject_global_styles,
    sidebar_brand,
    render_header,
    section_box,
    render_color_kpis,
    render_scanner_pills,
)
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

history = pd.read_csv(price_file)

with st.sidebar:
    sidebar_brand()

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

metrics = compute_metrics(history_filtered, selected_universe)
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

all_sectors = sorted(metrics_liquid["sector"].dropna().unique().tolist())

with st.sidebar:
    search_text = st.text_input("Search symbol or company")
    selected_sectors = st.multiselect("Sector", options=all_sectors, default=[])

filtered_metrics = apply_table_filters(metrics_liquid, search_text, selected_sectors)

q_screen = run_qullamaggie_screen(filtered_metrics)
m_screen = run_minervini_screen(filtered_metrics)
c_screen = run_consensus_screen(q_screen, m_screen)

safe_universe = (
    universe_mode.lower()
    .replace(" ", "_")
    .replace("(", "")
    .replace(")", "")
)

render_header(universe_mode)

render_color_kpis(
    universe_count=len(selected_universe),
    liquid_count=metrics_after_liquidity,
    q_count=len(q_screen),
    m_count=len(m_screen),
)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
render_scanner_pills()

top_tab, q_tab, m_tab, c_tab, metrics_tab = st.tabs([
    "Overview",
    "Qullamaggie",
    "Minervini",
    "Consensus",
    "Metrics",
])

with top_tab:
    left, right = st.columns([1.2, 1], gap="large")

    with left:
        section_box(
            "Summary",
            "Market Overview",
            "Coverage and filter status for the current scanner run."
        )
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Source Rows", source_rows, border=True)
        a2.metric("Universe Used", universe_rows_used, border=True)
        a3.metric("Pre-Liquidity", metrics_before_liquidity, border=True)
        a4.metric("Post-Liquidity", metrics_after_liquidity, border=True)

    with right:
        section_box(
            "Exports",
            "Download Files",
            "Export scanner outputs for review."
        )
        st.download_button(
            label=f"Download Qullamaggie CSV ({universe_mode})",
            data=dataframe_to_csv_bytes(q_screen),
            file_name=f"qullamaggie_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.download_button(
            label=f"Download Minervini CSV ({universe_mode})",
            data=dataframe_to_csv_bytes(m_screen),
            file_name=f"minervini_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.download_button(
            label=f"Download Consensus CSV ({universe_mode})",
            data=dataframe_to_csv_bytes(c_screen),
            file_name=f"consensus_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True
        )

with q_tab:
    section_box(
        "Scanner",
        "Qullamaggie",
        "Momentum expansion candidates from the filtered universe."
    )
    if q_screen.empty:
        st.info("No Qullamaggie matches yet.")
    else:
        st.dataframe(q_screen.round(2), use_container_width=True, hide_index=True)

with m_tab:
    section_box(
        "Scanner",
        "Minervini",
        "Trend template candidates from the filtered universe."
    )
    if m_screen.empty:
        st.info("No Minervini matches yet.")
    else:
        st.dataframe(m_screen.round(2), use_container_width=True, hide_index=True)

with c_tab:
    section_box(
        "Scanner",
        "Consensus",
        "Stocks that appear in both scanners."
    )
    if c_screen.empty:
        st.info("No consensus names yet.")
    else:
        st.dataframe(c_screen.round(2), use_container_width=True, hide_index=True)

with metrics_tab:
    section_box(
        "Metrics",
        "Filtered Metrics",
        "Core trend, liquidity, and RS inputs."
    )
    if filtered_metrics.empty:
        st.info("No metrics available.")
    else:
        st.dataframe(filtered_metrics.round(2), use_container_width=True, hide_index=True)
