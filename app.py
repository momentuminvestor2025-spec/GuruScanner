import os
from datetime import datetime

import pandas as pd
import streamlit as st

from components.styles import (
    inject_global_styles,
    sidebar_brand,
    render_topbar,
    render_stat_cards,
    render_market_strip,
    tab_header,
    render_pill_row,
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

st.set_page_config(page_title="Momentum Scanner", layout="wide")
inject_global_styles()

price_file = "data/latest_prices.csv"

if not os.path.exists(price_file):
    st.error("No cached price file found. Please generate latest_prices.csv first.")
    st.stop()

if os.path.getsize(price_file) == 0:
    st.error("latest_prices.csv exists but is empty. Please regenerate the file.")
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

scan_time_text = datetime.now().strftime("%b %d, %Y at %I:%M:%S %p")

render_topbar(scan_time_text)

stat_cards = [
    {
        "label": "Universe",
        "value": f"{len(selected_universe):,}",
        "sub": universe_mode,
        "accent": "stat-accent-blue",
    },
    {
        "label": "Total Scanned",
        "value": f"{metrics_before_liquidity:,}",
        "sub": "All stocks processed",
        "accent": "stat-accent-purple",
    },
    {
        "label": "Qullamaggie",
        "value": f"{len(q_screen):,}",
        "sub": "RS strong + momentum",
        "accent": "stat-accent-green",
    },
    {
        "label": "Minervini",
        "value": f"{len(m_screen):,}",
        "sub": "Trend template",
        "accent": "stat-accent-amber",
    },
    {
        "label": "Consensus",
        "value": f"{len(c_screen):,}",
        "sub": "2+ scanners agree",
        "accent": "stat-accent-red",
    },
]

render_stat_cards(stat_cards)

market_strip_items = [
    {"label": "Nifty 50", "value": "Live soon", "sub": "Index pulse", "tone": "mini-neutral"},
    {"label": "Nifty Next 50", "value": "Live soon", "sub": "Leadership bench", "tone": "mini-neutral"},
    {"label": "Midcap 150", "value": "Live soon", "sub": "Risk appetite", "tone": "mini-neutral"},
    {"label": "India VIX", "value": "Live soon", "sub": "Volatility regime", "tone": "mini-neutral"},
    {"label": "Breadth", "value": f"{metrics_after_liquidity:,}", "sub": "Liquid names surviving", "tone": "mini-pos"},
    {"label": "Risk Control", "value": "OK", "sub": "Liquidity filter active", "tone": "mini-pos"},
]

render_market_strip(market_strip_items)

overview_tab, q_tab, m_tab, c_tab, metrics_tab = st.tabs(
    ["Overview", "Qullamaggie", "Minervini", "Consensus", "Metrics"]
)

with overview_tab:
    tab_header(
        "Scanner Overview",
        "Indian Market Momentum Workspace",
        "Use the scanner tabs for stock selection and export-ready outputs."
    )

st.markdown("<div class='overview-panel'>", unsafe_allow_html=True)
o1, o2, o3, o4 = st.columns(4, gap="small")
o1.metric("Source Rows", source_rows, border=True)
o2.metric("Universe Rows Used", universe_rows_used, border=True)
o3.metric("Post-Liquidity", metrics_after_liquidity, border=True)
o4.metric("Strict Liquidity", "On" if strict_liquidity else "Off", border=True)
st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1], gap="large")

    with left:
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

        tab_header(
            "Breadth",
            "Sector Strength",
            "Most represented sectors among the filtered Indian universe."
        )
        if top_sectors.empty:
            st.info("No sector summary available.")
        else:
            st.dataframe(
                top_sectors.round(2),
                use_container_width=True,
                hide_index=True
            )

    with right:
        tab_header(
            "Filters",
            "Current Rules",
            "Applied before scanner results are generated."
        )
        render_pill_row([
            (universe_mode, "pill-blue"),
            ("Liquidity On" if enable_liquidity else "Liquidity Off", "pill-green"),
            ("Strict" if strict_liquidity else "Relaxed", "pill-amber"),
        ])
        st.write(f"**Min Price:** {min_price:,.2f}")
        st.write(f"**Min 20D Avg Volume:** {int(min_avg_volume_20):,}")
        st.write(f"**Min 20D Avg Traded Value:** {int(min_avg_traded_value_20):,}")

with q_tab:
    tab_header(
        "Qullamaggie",
        "Qullamaggie Scanner",
        "Momentum expansion candidates from the filtered Indian universe."
    )

    tq1, tq2 = st.columns([0.22, 0.78], gap="small")
    with tq1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(q_screen),
            file_name=f"qullamaggie_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_q_tab"
        )
    with tq2:
        render_pill_row([
            (f"{len(q_screen)} matches", "pill-green"),
            ("RS + momentum", "pill-blue"),
        ])

    if q_screen.empty:
        st.info("No Qullamaggie matches yet.")
    else:
        q_cols = [
            "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
            "rs_score", "dist_52w_high_pct", "volume_surge", "avg_traded_value_20"
        ]
        st.dataframe(
            q_screen[q_cols].round(2),
            use_container_width=True,
            hide_index=True
        )

with m_tab:
    tab_header(
        "Minervini",
        "Minervini Scanner",
        "Trend template candidates from the filtered Indian universe."
    )

    tm1, tm2 = st.columns([0.22, 0.78], gap="small")
    with tm1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(m_screen),
            file_name=f"minervini_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_m_tab"
        )
    with tm2:
        render_pill_row([
            (f"{len(m_screen)} matches", "pill-amber"),
            ("Trend template", "pill-purple"),
        ])

    if m_screen.empty:
        st.info("No Minervini matches yet.")
    else:
        m_cols = [
            "symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
            "rs_score", "ma_aligned", "near_high", "avg_traded_value_20"
        ]
        st.dataframe(
            m_screen[m_cols].round(2),
            use_container_width=True,
            hide_index=True
        )

with c_tab:
    tab_header(
        "Consensus",
        "Consensus Scanner",
        "Stocks appearing in both major scanners."
    )

    tc1, tc2 = st.columns([0.22, 0.78], gap="small")
    with tc1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(c_screen),
            file_name=f"consensus_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_c_tab"
        )
    with tc2:
        render_pill_row([
            (f"{len(c_screen)} matches", "pill-red"),
            ("2 scanners agree", "pill-blue"),
        ])

    if c_screen.empty:
        st.info("No consensus names yet.")
    else:
        st.dataframe(
            c_screen.round(2),
            use_container_width=True,
            hide_index=True
        )

with metrics_tab:
    tab_header(
        "Metrics",
        "Filtered Metrics",
        "Core ranking, liquidity, and trend data for the selected universe."
    )

    tx1, tx2 = st.columns([0.22, 0.78], gap="small")
    with tx1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(filtered_metrics),
            file_name=f"metrics_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_metrics_tab"
        )
    with tx2:
        render_pill_row([
            (f"{len(filtered_metrics)} rows", "pill-blue"),
            ("Filtered universe", "pill-green"),
        ])

    if filtered_metrics.empty:
        st.info("No metrics available.")
    else:
        metrics_cols = [
            "symbol", "company", "sector", "close",
            "avg_volume_20", "avg_traded_value_20",
            "daily_pct", "weekly_pct", "rs_score",
            "dist_52w_high_pct", "range_pos_20", "volume_surge"
        ]
        st.dataframe(
            filtered_metrics[metrics_cols].round(2),
            use_container_width=True,
            hide_index=True
        )
