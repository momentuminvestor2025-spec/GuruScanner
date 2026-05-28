import os
import re
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from components.styles import (
    inject_global_styles,
    sidebar_brand,
    render_topbar,
    render_stat_cards,
    render_market_strip,
    tab_header,
    render_pill_row,
    render_breadth_section_css,
    render_breadth_card,
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
render_breadth_section_css()


@st.cache_data(ttl=300, show_spinner=False)
def get_nse_market_strip(metrics_after_liquidity_value: int):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    }

    target_labels = {
        "NIFTY 50": "Nifty 50",
        "NIFTY SMALLCAP 250": "Nifty Smallcap 250",
        "NIFTY 500": "NIFTY 500",
        "INDIA VIX": "Nifty India Vix",
    }

    fallback = [
        {"label": "Nifty 50", "value": "NA", "sub": "Unavailable", "tone": "mini-neutral"},
        {"label": "Nifty Smallcap 250", "value": "NA", "sub": "Unavailable", "tone": "mini-neutral"},
        {"label": "NIFTY 500", "value": "NA", "sub": "Unavailable", "tone": "mini-neutral"},
        {"label": "Nifty India Vix", "value": "NA", "sub": "Unavailable", "tone": "mini-neutral"},
        {"label": "A/D Ratio", "value": "NA", "sub": "Unavailable", "tone": "mini-neutral"},
        {"label": "Risk Control", "value": "OK", "sub": "Liquidity filter active", "tone": "mini-pos"},
    ]

    try:
        session = requests.Session()
        session.get("https://www.nseindia.com/", headers=headers, timeout=20)

        indices_response = session.get(
            "https://www.nseindia.com/api/allIndices",
            headers=headers,
            timeout=20
        )
        indices_response.raise_for_status()
        indices_payload = indices_response.json()
        indices_rows = indices_payload.get("data", [])
        indices_df = pd.DataFrame(indices_rows)

        if indices_df.empty or "index" not in indices_df.columns:
            return fallback

        indices_df["index"] = indices_df["index"].astype(str).str.strip()

        advance_response = session.get(
            "https://www.nseindia.com/market-data/advance",
            headers=headers,
            timeout=20
        )
        advance_response.raise_for_status()
        advance_text = advance_response.text

        adv_match = re.search(r"Advance\s*-\s*(\d+)", advance_text)
        dec_match = re.search(r"Decline\s*-\s*(\d+)", advance_text)
        unc_match = re.search(r"Unchanged\s*-\s*(\d+)", advance_text)

        advances = int(adv_match.group(1)) if adv_match else None
        declines = int(dec_match.group(1)) if dec_match else None
        unchanged = int(unc_match.group(1)) if unc_match else None

        if advances is not None and declines is not None and declines > 0:
            ad_ratio = round(advances / declines, 2)
            ad_sub = f"{advances} adv / {declines} dec"
            ad_tone = "mini-pos" if ad_ratio >= 1 else "mini-neg"
        else:
            ad_ratio = None
            ad_sub = "Unavailable"
            ad_tone = "mini-neutral"

        def tone_for(name: str, pct_value):
            try:
                pct = float(str(pct_value).replace("%", "").replace(",", "").strip())
            except Exception:
                return "mini-neutral"
            if name == "INDIA VIX":
                return "mini-neutral"
            if pct > 0:
                return "mini-pos"
            if pct < 0:
                return "mini-neg"
            return "mini-neutral"

        items = []

        for raw_name, display_label in target_labels.items():
            row = indices_df[indices_df["index"] == raw_name]
            if row.empty:
                items.append({
                    "label": display_label,
                    "value": "NA",
                    "sub": "Unavailable",
                    "tone": "mini-neutral",
                })
                continue

            row = row.iloc[0]
            current = row.get("last", row.get("lastPrice", "NA"))
            pct = row.get("percentChange", row.get("percChange", "NA"))

            current_text = str(current).strip()
            pct_text_raw = str(pct).strip()

            if pct_text_raw not in ["NA", "None", "nan", ""]:
                pct_text = f"{pct_text_raw}% today" if pct_text_raw.startswith("-") else f"+{pct_text_raw}% today"
            else:
                pct_text = "Unavailable"

            items.append({
                "label": display_label,
                "value": current_text,
                "sub": pct_text,
                "tone": tone_for(raw_name, pct_text_raw),
            })

        items.append({
            "label": "A/D Ratio",
            "value": f"{ad_ratio:.2f}" if ad_ratio is not None else "NA",
            "sub": ad_sub if unchanged is None else f"{ad_sub} / {unchanged} unc",
            "tone": ad_tone,
        })

        items.append({
            "label": "Risk Control",
            "value": "OK",
            "sub": "Liquidity filter active",
            "tone": "mini-pos",
        })

        return items

    except Exception:
        return fallback


@st.cache_data(ttl=300, show_spinner=False)
def get_market_breadth_data(filtered_metrics: pd.DataFrame, q_screen: pd.DataFrame, m_screen: pd.DataFrame):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    }

    data = {
        "indices": {},
        "advances": None,
        "declines": None,
        "unchanged": None,
        "ad_ratio": None,
    }

    try:
        session = requests.Session()
        session.get("https://www.nseindia.com/", headers=headers, timeout=20)

        indices_response = session.get("https://www.nseindia.com/api/allIndices", headers=headers, timeout=20)
        indices_response.raise_for_status()
        indices_payload = indices_response.json()
        indices_df = pd.DataFrame(indices_payload.get("data", []))

        if not indices_df.empty and "index" in indices_df.columns:
            indices_df["index"] = indices_df["index"].astype(str).str.strip()
            wanted = ["NIFTY 50", "NIFTY SMALLCAP 250", "NIFTY 500", "INDIA VIX"]
            for idx in wanted:
                row = indices_df[indices_df["index"] == idx]
                if not row.empty:
                    row = row.iloc[0]
                    data["indices"][idx] = {
                        "last": row.get("last", row.get("lastPrice", "NA")),
                        "pct": row.get("percentChange", row.get("percChange", "NA")),
                    }

        adv_response = session.get("https://www.nseindia.com/market-data/advance", headers=headers, timeout=20)
        adv_response.raise_for_status()
        adv_text = adv_response.text

        adv_match = re.search(r"Advance\s*-\s*(\d+)", adv_text)
        dec_match = re.search(r"Decline\s*-\s*(\d+)", adv_text)
        unc_match = re.search(r"Unchanged\s*-\s*(\d+)", adv_text)

        data["advances"] = int(adv_match.group(1)) if adv_match else None
        data["declines"] = int(dec_match.group(1)) if dec_match else None
        data["unchanged"] = int(unc_match.group(1)) if unc_match else None

        if data["advances"] is not None and data["declines"] not in [None, 0]:
            data["ad_ratio"] = round(data["advances"] / data["declines"], 2)

    except Exception:
        pass

    df = filtered_metrics.copy()

    if not df.empty:
        for col in ["daily_pct", "weekly_pct", "monthly_pct", "close", "rs_score", "dist_52w_high_pct", "sma_50", "sma_100", "sma_200"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    data["above_50dma_pct"] = round((df["close"] > df["sma_50"]).mean() * 100, 2) if {"close", "sma_50"}.issubset(df.columns) and len(df) else None
    data["above_100dma_pct"] = round((df["close"] > df["sma_100"]).mean() * 100, 2) if {"close", "sma_100"}.issubset(df.columns) and len(df) else None
    data["above_200dma_pct"] = round((df["close"] > df["sma_200"]).mean() * 100, 2) if {"close", "sma_200"}.issubset(df.columns) and len(df) else None

    data["new_highs"] = int((df["dist_52w_high_pct"] >= -2).sum()) if "dist_52w_high_pct" in df.columns else 0
    data["new_lows"] = int((df["dist_52w_high_pct"] <= -30).sum()) if "dist_52w_high_pct" in df.columns else 0

    data["stage2_entries"] = len(q_screen)
    data["stage2_exits"] = int((df["close"] < df["sma_50"]).sum()) if {"close", "sma_50"}.issubset(df.columns) and len(df) else 0
    data["stage2_net"] = data["stage2_entries"] - data["stage2_exits"]

    if "sector" in df.columns and "rs_score" in df.columns:
        data["top_sectors"] = (
            df.groupby("sector", dropna=False)
            .agg(avg_rs=("rs_score", "mean"), count=("sector", "count"))
            .sort_values(["avg_rs", "count"], ascending=[False, False])
            .reset_index()
            .head(5)
        )
    else:
        data["top_sectors"] = pd.DataFrame()

    if "symbol" in df.columns and "weekly_pct" in df.columns:
        rs_df = df[["symbol", "weekly_pct"]].dropna().sort_values("weekly_pct", ascending=False)
        data["rs_winners"] = rs_df.head(5)
        data["rs_losers"] = rs_df.tail(5).sort_values("weekly_pct", ascending=True)
    else:
        data["rs_winners"] = pd.DataFrame()
        data["rs_losers"] = pd.DataFrame()

    if "daily_pct" in df.columns:
        data["up_4"] = int((df["daily_pct"] >= 4).sum())
        data["down_4"] = int((df["daily_pct"] <= -4).sum())
    else:
        data["up_4"] = 0
        data["down_4"] = 0

    if "weekly_pct" in df.columns:
        data["up_10"] = int((df["weekly_pct"] >= 10).sum())
        data["down_10"] = int((df["weekly_pct"] <= -10).sum())
    else:
        data["up_10"] = 0
        data["down_10"] = 0

    return data


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

    universe_mode = st.selectbox(
        "Universe",
        options=["Nifty 500", "Nifty 750 (Total Market)"],
        index=0,
    )

    strict_liquidity = st.checkbox(
        "Strict liquidity mode",
        value=(universe_mode == "Nifty 750 (Total Market)")
    )

    enable_liquidity = st.checkbox("Enable Liquidity Filters", value=True)


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
        step=5.0,
    )

    min_avg_volume_20 = st.number_input(
        "Min 20D Avg Volume",
        min_value=0,
        value=int(defaults["min_avg_volume_20"]),
        step=50000,
    )

    min_avg_traded_value_20 = st.number_input(
        "Min 20D Avg Traded Value",
        min_value=0,
        value=int(defaults["min_avg_traded_value_20"]),
        step=10000000,
    )

metrics_liquid, metrics_before_liquidity, metrics_after_liquidity = apply_liquidity_filters(
    metrics_df=metrics,
    min_price=min_price,
    min_avg_volume_20=min_avg_volume_20,
    min_avg_traded_value_20=min_avg_traded_value_20,
    enable_filter=enable_liquidity,
)

all_sectors = sorted(metrics_liquid["sector"].dropna().unique().tolist()) if "sector" in metrics_liquid.columns else []

with st.sidebar:
    search_text = st.text_input("Search symbol or company")
    selected_sectors = st.multiselect("Sector", options=all_sectors, default=[])

filtered_metrics = apply_table_filters(metrics_liquid, search_text, selected_sectors)

q_screen = run_qullamaggie_screen(filtered_metrics)
m_screen = run_minervini_screen(filtered_metrics)
c_screen = run_consensus_screen(q_screen, m_screen)

breadth_data = get_market_breadth_data(filtered_metrics, q_screen, m_screen)

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

market_strip_items = get_nse_market_strip(metrics_after_liquidity)
render_market_strip(market_strip_items)

overview_tab, breadth_tab, q_tab, m_tab, c_tab, metrics_tab = st.tabs(
    ["Overview", "Market Breadth", "Qullamaggie", "Minervini", "Consensus", "Metrics"]
)

with overview_tab:
    tab_header(
        "Scanner Overview",
        "Indian Market Momentum Workspace",
        "Use the scanner tabs for stock selection and export-ready outputs.",
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
        if "sector" in filtered_metrics.columns and "symbol" in filtered_metrics.columns and "rs_score" in filtered_metrics.columns:
            top_sectors = (
                filtered_metrics.groupby("sector", dropna=False)
                .agg(
                    stocks=("symbol", "count"),
                    avg_rs=("rs_score", "mean"),
                )
                .sort_values(["stocks", "avg_rs"], ascending=[False, False])
                .reset_index()
                .head(10)
            )
        else:
            top_sectors = pd.DataFrame()

        tab_header(
            "Breadth",
            "Sector Strength",
            "Most represented sectors among the filtered Indian universe.",
        )

        if top_sectors.empty:
            st.info("No sector summary available.")
        else:
            st.dataframe(
                top_sectors.round(2),
                use_container_width=True,
                hide_index=True,
            )

    with right:
        tab_header(
            "Filters",
            "Current Rules",
            "Applied before scanner results are generated.",
        )

        render_pill_row([
            (universe_mode, "pill-blue"),
            ("Liquidity On" if enable_liquidity else "Liquidity Off", "pill-green"),
            ("Strict" if strict_liquidity else "Relaxed", "pill-amber"),
        ])

        st.write(f"**Min Price:** {min_price:,.2f}")
        st.write(f"**Min 20D Avg Volume:** {int(min_avg_volume_20):,}")
        st.write(f"**Min 20D Avg Traded Value:** {int(min_avg_traded_value_20):,}")

with breadth_tab:
    tab_header(
        "Market Breadth",
        "Market Recap",
        "Live market pulse, breadth snapshot, movers, sector rotation, and RS leadership.",
    )

    n50 = breadth_data["indices"].get("NIFTY 50", {})
    ns250 = breadth_data["indices"].get("NIFTY SMALLCAP 250", {})
    n500 = breadth_data["indices"].get("NIFTY 500", {})
    vix = breadth_data["indices"].get("INDIA VIX", {})

    n500_pct = n500.get("pct", "NA")
    pulse_class = "breadth-big"
    try:
        if float(str(n500_pct)) < 0:
            pulse_class = "breadth-big neg-text"
    except Exception:
        pulse_class = "breadth-big"

    market_pulse_html = f"""
    <div class="{pulse_class}">{n500_pct}%</div>
    <div class="breadth-big-sub">NIFTY 500 daily return</div>

    <div class="breadth-mini-grid">
        <div class="breadth-stat">
            <div class="breadth-stat-label">Nifty 50</div>
            <div class="breadth-stat-value">{n50.get('last', 'NA')}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">A/D Ratio</div>
            <div class="breadth-stat-value">{breadth_data.get('ad_ratio', 'NA')}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">Nifty Smallcap 250</div>
            <div class="breadth-stat-value">{ns250.get('last', 'NA')}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">India VIX</div>
            <div class="breadth-stat-value">{vix.get('last', 'NA')}</div>
        </div>
    </div>
    """

    breadth_snapshot_html = f"""
    <div class="breadth-list">
        <div class="breadth-row"><span class="breadth-row-left">&gt; 200 DMA</span><span class="breadth-row-right">{breadth_data.get('above_200dma_pct', 'NA')}%</span></div>
        <div class="breadth-row"><span class="breadth-row-left">&gt; 100 DMA</span><span class="breadth-row-right">{breadth_data.get('above_100dma_pct', 'NA')}%</span></div>
        <div class="breadth-row"><span class="breadth-row-left">&gt; 50 DMA</span><span class="breadth-row-right">{breadth_data.get('above_50dma_pct', 'NA')}%</span></div>
        <div class="breadth-row"><span class="breadth-row-left">52W Highs</span><span class="breadth-row-right pos-text">{breadth_data.get('new_highs', 0)}</span></div>
        <div class="breadth-row"><span class="breadth-row-left">52W Lows</span><span class="breadth-row-right neg-text">{breadth_data.get('new_lows', 0)}</span></div>
        <div class="breadth-row"><span class="breadth-row-left">Advance / Decline</span><span class="breadth-row-right">{breadth_data.get('advances', 'NA')} / {breadth_data.get('declines', 'NA')}</span></div>
    </div>
    """

    big_movers_html = f"""
    <div class="breadth-mini-grid">
        <div class="breadth-stat">
            <div class="breadth-stat-label">Single Day Up 4%+</div>
            <div class="breadth-stat-value pos-text">{breadth_data.get('up_4', 0)}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">Single Day Down 4%+</div>
            <div class="breadth-stat-value neg-text">{breadth_data.get('down_4', 0)}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">5-Day Up 10%+</div>
            <div class="breadth-stat-value pos-text">{breadth_data.get('up_10', 0)}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">5-Day Down 10%+</div>
            <div class="breadth-stat-value neg-text">{breadth_data.get('down_10', 0)}</div>
        </div>
    </div>
    """

    stage2_html = f"""
    <div class="breadth-mini-grid">
        <div class="breadth-stat">
            <div class="breadth-stat-label">Entries</div>
            <div class="breadth-stat-value pos-text">{breadth_data.get('stage2_entries', 0)}</div>
        </div>
        <div class="breadth-stat">
            <div class="breadth-stat-label">Exits</div>
            <div class="breadth-stat-value neg-text">{breadth_data.get('stage2_exits', 0)}</div>
        </div>
        <div class="breadth-stat" style="grid-column: 1 / span 2;">
            <div class="breadth-stat-label">Net</div>
            <div class="breadth-stat-value {'pos-text' if breadth_data.get('stage2_net', 0) >= 0 else 'neg-text'}">{breadth_data.get('stage2_net', 0):+d}</div>
        </div>
    </div>
    """

    top_sectors = breadth_data.get("top_sectors", pd.DataFrame())
    if top_sectors.empty:
        sector_rotation_html = "<div class='breadth-big-sub'>No sector data available</div>"
    else:
        sector_rotation_html = "<div class='breadth-list'>"
        for _, row in top_sectors.iterrows():
            sector_rotation_html += f"""
            <div class="breadth-row">
                <span class="breadth-row-left">{row['sector']}</span>
                <span class="breadth-row-right">{row['avg_rs']:.1f}</span>
            </div>
            """
        sector_rotation_html += "</div>"

    rs_winners = breadth_data.get("rs_winners", pd.DataFrame())
    rs_losers = breadth_data.get("rs_losers", pd.DataFrame())

    rs_html = "<div class='breadth-mini-grid'><div><div class='breadth-stat-label'>Winners</div><div class='breadth-list'>"
    if not rs_winners.empty:
        for _, row in rs_winners.iterrows():
            rs_html += f"""
            <div class="breadth-row">
                <span class="breadth-row-left">{row['symbol']}</span>
                <span class="breadth-row-right pos-text">{row['weekly_pct']:.1f}</span>
            </div>
            """
    rs_html += "</div></div><div><div class='breadth-stat-label'>Losers</div><div class='breadth-list'>"
    if not rs_losers.empty:
        for _, row in rs_losers.iterrows():
            rs_html += f"""
            <div class="breadth-row">
                <span class="breadth-row-left">{row['symbol']}</span>
                <span class="breadth-row-right neg-text">{row['weekly_pct']:.1f}</span>
            </div>
            """
    rs_html += "</div></div></div>"

    st.markdown("<div class='breadth-grid'>", unsafe_allow_html=True)
    render_breadth_card("Market Pulse", market_pulse_html)
    render_breadth_card("Breadth Snapshot", breadth_snapshot_html)
    render_breadth_card("Big Movers", big_movers_html)
    render_breadth_card("Stage 2 Pipeline", stage2_html)
    render_breadth_card("Sector Rotation", sector_rotation_html)
    render_breadth_card("RS Movers", rs_html)
    st.markdown("</div>", unsafe_allow_html=True)

with q_tab:
    tab_header(
        "Qullamaggie",
        "Qullamaggie Scanner",
        "Momentum expansion candidates from the filtered Indian universe.",
    )

    tq1, tq2 = st.columns([0.22, 0.78], gap="small")
    with tq1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(q_screen),
            file_name=f"qullamaggie_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_q_tab",
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
            "symbol",
            "company",
            "sector",
            "close",
            "daily_pct",
            "weekly_pct",
            "rs_score",
            "dist_52w_high_pct",
            "volume_surge",
            "avg_traded_value_20",
        ]
        q_available_cols = [c for c in q_cols if c in q_screen.columns]
        st.dataframe(
            q_screen[q_available_cols].round(2),
            use_container_width=True,
            hide_index=True,
        )

with m_tab:
    tab_header(
        "Minervini",
        "Minervini Scanner",
        "Trend template candidates from the filtered Indian universe.",
    )

    tm1, tm2 = st.columns([0.22, 0.78], gap="small")
    with tm1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(m_screen),
            file_name=f"minervini_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_m_tab",
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
            "symbol",
            "company",
            "sector",
            "close",
            "daily_pct",
            "weekly_pct",
            "rs_score",
            "ma_aligned",
            "near_high",
            "avg_traded_value_20",
        ]
        m_available_cols = [c for c in m_cols if c in m_screen.columns]
        st.dataframe(
            m_screen[m_available_cols].round(2),
            use_container_width=True,
            hide_index=True,
        )

with c_tab:
    tab_header(
        "Consensus",
        "Consensus Scanner",
        "Stocks appearing in both major scanners.",
    )

    tc1, tc2 = st.columns([0.22, 0.78], gap="small")
    with tc1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(c_screen),
            file_name=f"consensus_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_c_tab",
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
            hide_index=True,
        )

with metrics_tab:
    tab_header(
        "Metrics",
        "Filtered Metrics",
        "Core ranking, liquidity, and trend data for the selected universe.",
    )

    tx1, tx2 = st.columns([0.22, 0.78], gap="small")
    with tx1:
        st.download_button(
            label="CSV",
            data=dataframe_to_csv_bytes(filtered_metrics),
            file_name=f"metrics_{safe_universe}.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_metrics_tab",
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
            "symbol",
            "company",
            "sector",
            "close",
            "avg_volume_20",
            "avg_traded_value_20",
            "daily_pct",
            "weekly_pct",
            "rs_score",
            "dist_52w_high_pct",
            "range_pos_20",
            "volume_surge",
        ]
        metrics_available_cols = [c for c in metrics_cols if c in filtered_metrics.columns]
        st.dataframe(
            filtered_metrics[metrics_available_cols].round(2),
            use_container_width=True,
            hide_index=True,
        )
