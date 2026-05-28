import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6f7fb;
            --panel: #ffffff;
            --panel-soft: #fbfcfe;
            --border: #e7ebf3;
            --text: #1f2937;
            --muted: #6b7280;
            --muted-2: #94a3b8;

            --blue: #4f8df7;
            --purple: #8b5cf6;
            --green: #10b981;
            --amber: #f59e0b;
            --red: #ef4444;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(79,141,247,0.08), transparent 20%),
                radial-gradient(circle at top right, rgba(139,92,246,0.06), transparent 18%),
                linear-gradient(180deg, #f7f9fc 0%, #f3f6fb 100%);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: rgba(255,255,255,0.88);
            border-right: 1px solid rgba(231,235,243,0.9);
            backdrop-filter: blur(12px);
        }

        .block-container {
            max-width: 1550px;
            padding-top: 0.7rem;
            padding-bottom: 1rem;
        }

        h1, h2, h3, h4 {
            color: var(--text) !important;
            letter-spacing: -0.02em;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.9rem;
        }

        .topbar-title {
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }

        .topbar-icon {
            width: 26px;
            height: 26px;
            border-radius: 8px;
            border: 2px solid var(--blue);
            color: var(--blue);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.9rem;
            background: #eef4ff;
            box-shadow: 0 8px 20px rgba(79,141,247,0.12);
        }

        .topbar-name {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text);
        }

        .topbar-sub {
            color: var(--muted);
            font-size: 0.83rem;
        }

        .toolbar-note {
            color: var(--muted);
            font-size: 0.83rem;
            text-align: right;
        }

        .stat-card {
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(231,235,243,0.95);
            border-radius: 16px;
            padding: 0.8rem 1rem;
            min-height: 96px;
            box-shadow:
                0 10px 30px rgba(15, 23, 42, 0.05),
                inset 0 1px 0 rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
        }

        .stat-label {
            color: var(--muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }

        .stat-value {
            color: var(--text);
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.25rem;
        }

        .stat-sub {
            color: var(--muted-2);
            font-size: 0.8rem;
        }

        .stat-accent-blue { box-shadow: inset 0 0 0 1px rgba(79,141,247,0.04), 0 10px 28px rgba(79,141,247,0.06); }
        .stat-accent-purple { box-shadow: inset 0 0 0 1px rgba(139,92,246,0.04), 0 10px 28px rgba(139,92,246,0.06); }
        .stat-accent-green { box-shadow: inset 0 0 0 1px rgba(16,185,129,0.04), 0 10px 28px rgba(16,185,129,0.06); }
        .stat-accent-amber { box-shadow: inset 0 0 0 1px rgba(245,158,11,0.04), 0 10px 28px rgba(245,158,11,0.06); }
        .stat-accent-red { box-shadow: inset 0 0 0 1px rgba(239,68,68,0.04), 0 10px 28px rgba(239,68,68,0.06); }

        .mini-strip {
            background: transparent;
            border: none;
            padding: 0.15rem 0;
            margin-top: 0.55rem;
            margin-bottom: 0.55rem;
        }

        .mini-box {
            position: relative;
            overflow: hidden;
            border-radius: 18px;
            padding: 0.95rem 1rem 0.9rem 1rem;
            min-height: 108px;
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.16), transparent 32%),
                linear-gradient(145deg, #0f1c36 0%, #0a1730 45%, #081224 100%);
            border: 1px solid rgba(98, 139, 255, 0.16);
            box-shadow:
                0 18px 35px rgba(8, 18, 36, 0.22),
                inset 0 1px 0 rgba(255,255,255,0.08),
                inset 0 -1px 0 rgba(255,255,255,0.03);
            transform: translateY(0);
        }

        .mini-box::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 18px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(79,141,247,0.18), transparent 26%);
            pointer-events: none;
        }

        .mini-label {
            position: relative;
            z-index: 1;
            color: rgba(226,232,240,0.82);
            font-size: 0.68rem;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .mini-value {
            position: relative;
            z-index: 1;
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 0.25rem;
            letter-spacing: -0.03em;
            color: #f8fafc;
            text-shadow: 0 3px 14px rgba(0,0,0,0.22);
        }

        .mini-sub {
            position: relative;
            z-index: 1;
            color: rgba(203,213,225,0.75);
            font-size: 0.82rem;
            line-height: 1.25;
        }

        .mini-pos {
            color: #22e6a3;
            text-shadow: 0 0 16px rgba(34,230,163,0.18);
        }

        .mini-neg {
            color: #ff6b6b;
            text-shadow: 0 0 16px rgba(255,107,107,0.16);
        }

        .mini-neutral {
            color: #ffbe5c;
            text-shadow: 0 0 16px rgba(255,190,92,0.16);
        }

        .tab-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(231,235,243,0.95);
            border-radius: 16px;
            padding: 0.95rem 1rem 0.8rem 1rem;
            margin-bottom: 0.8rem;
            box-shadow:
                0 10px 30px rgba(15,23,42,0.05),
                inset 0 1px 0 rgba(255,255,255,0.8);
        }

        .tab-label {
            color: var(--muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-bottom: 0.2rem;
        }

        .tab-title {
            color: var(--text);
            font-size: 1.12rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .tab-sub {
            color: var(--muted);
            font-size: 0.86rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.3rem;
        }

        button[role="tab"] {
            background: rgba(255,255,255,0.66) !important;
            color: var(--muted) !important;
            border-radius: 11px !important;
            padding: 0.5rem 0.95rem !important;
            font-weight: 700 !important;
            border: 1px solid rgba(231,235,243,0.9) !important;
            margin-right: 0.15rem !important;
            box-shadow: none !important;
        }

        button[role="tab"][aria-selected="true"] {
            color: var(--text) !important;
            background: #ffffff !important;
            border: 1px solid rgba(210,219,232,1) !important;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06) !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(231,235,243,0.95);
            border-radius: 16px;
            overflow: hidden;
            background: rgba(255,255,255,0.95);
            box-shadow: 0 10px 28px rgba(15,23,42,0.04);
        }

        div[data-testid="stDataFrame"] [role="columnheader"] {
            background: #f8fafc !important;
            color: #6b7280 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stDataFrame"] [role="gridcell"] {
            background: #ffffff !important;
            color: var(--text) !important;
            border-color: #eef2f7 !important;
        }

        .pill-row {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }

        .pill {
            padding: 0.32rem 0.65rem;
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 700;
            border: 1px solid transparent;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.45);
        }

        .pill-blue { background: #eef4ff; color: #336ad4; border-color: #d8e7ff; }
        .pill-green { background: #ebfbf4; color: #0f9f67; border-color: #d2f5e5; }
        .pill-purple { background: #f4efff; color: #7c4ce0; border-color: #e6dbff; }
        .pill-amber { background: #fff6e8; color: #ca8a04; border-color: #fde7bf; }
        .pill-red { background: #feeff1; color: #d33a4c; border-color: #ffd7dd; }

        .stDownloadButton button,
        .stButton button {
            border-radius: 12px !important;
            border: 1px solid rgba(231,235,243,0.95) !important;
            background: rgba(255,255,255,0.92) !important;
            color: var(--text) !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 20px rgba(15,23,42,0.05) !important;
        }

        .stTextInput input,
        .stNumberInput input,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            background: rgba(255,255,255,0.9) !important;
            color: var(--text) !important;
            border: 1px solid rgba(231,235,243,0.95) !important;
            border-radius: 12px !important;
            box-shadow: 0 6px 18px rgba(15,23,42,0.03) !important;
        }

        div[data-testid="metric-container"] {
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(231,235,243,0.95);
            border-radius: 16px;
            padding: 0.8rem 0.9rem;
            min-height: 94px;
            box-shadow:
                0 10px 28px rgba(15,23,42,0.04),
                inset 0 1px 0 rgba(255,255,255,0.75);
        }

        div[data-testid="metric-container"] label {
            color: var(--muted) !important;
            text-transform: uppercase;
            font-size: 0.73rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em;
        }

        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.55rem !important;
            font-weight: 800 !important;
        }

        .overview-panel {
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(231,235,243,0.95);
            border-radius: 16px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 10px 28px rgba(15,23,42,0.04);
        }

        .sidebar-brand {
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 800;
            margin-bottom: 0.15rem;
        }

        .sidebar-sub {
            color: var(--muted);
            font-size: 0.8rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-brand">Momentum Scanner</div>
        <div class="sidebar-sub">Indian market scanner workspace</div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(scan_time_text: str):
    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-title">
                <div class="topbar-icon">↗</div>
                <div>
                    <div class="topbar-name">Momentum Scanner</div>
                    <div class="topbar-sub">Last scan: {scan_time_text}</div>
                </div>
            </div>
            <div class="toolbar-note">Indian market layout • NSE-first workflow</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_cards(cards):
    cols = st.columns(len(cards), gap="small")
    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="stat-card {card['accent']}">
                    <div class="stat-label">{card['label']}</div>
                    <div class="stat-value">{card['value']}</div>
                    <div class="stat-sub">{card['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_market_strip(items):
    st.markdown("<div class='mini-strip'>", unsafe_allow_html=True)
    cols = st.columns(len(items), gap="small")
    for col, item in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class="mini-box">
                    <div class="mini-label">{item['label']}</div>
                    <div class="mini-value {item.get('tone', '')}">{item['value']}</div>
                    <div class="mini-sub">{item['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def tab_header(label: str, title: str, sub: str):
    st.markdown(
        f"""
        <div class="tab-card">
            <div class="tab-label">{label}</div>
            <div class="tab-title">{title}</div>
            <div class="tab-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pill_row(pills):
    html = "<div class='pill-row'>"
    for text, cls in pills:
        html += f"<span class='pill {cls}'>{text}</span>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
