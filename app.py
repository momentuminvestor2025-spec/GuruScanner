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
    st.error("latest_prices.csv exists but is empty. Please regenerate the file.")
    st.stop()

try:
    history = pd.read_csv(price_file)
except pd.errors.EmptyDataError:
    st.error("latest_prices.csv has no valid CSV content. Please regenerate it.")
    st.stop()

with st.sidebar:
    sidebar_brand()
    st.markdown(
        "<div class='mini-note'>Configure universe, liquidity, and sector filters.</div>",
        unsafe_allow_html=True,
    )

    universe_mode = st.selectbox(
        "Universe",
        options=["Nifty 500", "Nifty 750 (Total Market)"],
        index=0,
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
    min_price = st.number_input(
        "Min Price",
        min_value=1.0,
        value=float(defaults["min_price"]),
        step=5.0
    )
    min_avg_volume_20 = st.number_input(
        "Min 20D Avg Volume",
        min_value=0,
        value=int(defaults["min_avg_volume_20"]),
        step=50000
    )
    min_avg_traded_value_20 = st.number_input(
        "Min 20D Avg Traded Value",
        min_value=0,
        value=int(defaults["min_avg_traded_value_20"]),
        step=10000000
    )

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

leaders = filtered_metrics.sort_values(
    ["rs_score", "dist_52w_high_pct"],
    ascending=[False, True]
).head(12)

unknown_count = int((filtered_metrics["company"] == "Unknown Company").sum())

safe_universe = (
    universe_mode.lower()
    .replace(" ", "_")
    .replace("(", "")
    .replace(")", "")
)

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
    st.write(f"**Min Price:** {min_price:,.2f}")
    st.write(f"**Min 20D Avg Volume:** {int(min_avg_volume_20):,}")
    st.write(f"**Min 20D Avg Traded Value:** {int(min_avg_traded_value_20):,}")
    st.write(f"**Search Universe:** {universe_mode}")
    st.write(f"**Strict Liquidity:** {'On' if strict_liquidity else 'Off'}")

    section_header(
        "Leaders",
        "Top RS Names",
        "Highest relative-strength stocks surviving all active filters."
    )

    leader_cols = [
        "symbol", "close", "rs_score", "dist_52w_high_pct",
        "avg_traded_value_20", "volume_surge"
    ]

    if leaders.empty:
        st.info("No leaders available after current filters.")
    else:
        st.dataframe(
            leaders[leader_cols].round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.2f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "avg_traded_value_20": st.column_config.NumberColumn("20D Avg Traded Value", format="%.0f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

    section_header(
        "Exports",
        "Download Scanner Outputs",
        "Export liquid-screened datasets for further review."
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
    st.download_button(
        label=f"Download Metrics CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(filtered_metrics),
        file_name=f"metrics_{safe_universe}.csv",
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
    "avg_volume_20", "avg_traded_value_20",
    "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
    "volume_surge", "badge"
]

with tabs[0]:
    section_header(
        "Scanner",
        f"Qullamaggie — {universe_mode}",
        "Momentum leaders with expansion characteristics and strong relative strength."
    )
    if q_screen.empty:
        st.info("No Qullamaggie matches yet.")
    else:
        st.dataframe(
            q_screen[scanner_cols].round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "daily_pct": st.column_config.NumberColumn("Daily %", format="%.2f"),
                "weekly_pct": st.column_config.NumberColumn("Weekly %", format="%.2f"),
                "avg_volume_20": st.column_config.NumberColumn("20D Avg Vol", format="%.0f"),
                "avg_traded_value_20": st.column_config.NumberColumn("20D Avg Traded Value", format="%.0f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.1f"),
                "atr_rs": st.column_config.NumberColumn("ATR RS", format="%.1f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "range_pos_20": st.column_config.NumberColumn("20D Range %", format="%.2f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

with tabs[1]:
    section_header(
        "Scanner",
        f"Minervini — {universe_mode}",
        "Trend template candidates from the liquid, filtered universe."
    )
    if m_screen.empty:
        st.info("No Minervini matches yet.")
    else:
        st.dataframe(
            m_screen[scanner_cols].round(2),
            use_container_width=True,
            hide_index=True
        )

with tabs[2]:
    section_header(
        "Scanner",
        f"Consensus — {universe_mode}",
        "Stocks appearing in both scanner models."
    )
    if c_screen.empty:
        st.info("No overlap names yet.")
    else:
        st.dataframe(
            c_screen.round(2),
            use_container_width=True,
            hide_index=True
        )

with tabs[3]:
    section_header(
        "Metrics",
        f"Metrics Preview — {universe_mode}",
        "Core ranking, liquidity, and trend inputs for the filtered universe."
    )
    metrics_cols = [
        "symbol", "company", "sector", "close",
        "avg_volume_20", "avg_traded_value_20",
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
    section_header(
        "Data",
        f"Filtered Price Preview — {universe_mode}",
        "First 100 price-history rows after universe filtering."
    )
    st.dataframe(
        history_filtered.head(100),
        use_container_width=True,
        hide_index=True
    )
