import streamlit as st


def inject_global_styles():
    st.markdown("""
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
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
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
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.75rem 0.95rem;
        min-height: 92px;
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

    .stat-accent-blue { box-shadow: inset 0 0 0 1px rgba(79,141,247,0.04); }
    .stat-accent-purple { box-shadow: inset 0 0 0 1px rgba(139,92,246,0.04); }
    .stat-accent-green { box-shadow: inset 0 0 0 1px rgba(16,185,129,0.04); }
    .stat-accent-amber { box-shadow: inset 0 0 0 1px rgba(245,158,11,0.04); }
    .stat-accent-red { box-shadow: inset 0 0 0 1px rgba(239,68,68,0.04); }

    .mini-strip {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.55rem 0.85rem;
        margin-top: 0.55rem;
        margin-bottom: 0.45rem;
    }

    .mini-box {
        display: flex;
        flex-direction: column;
        gap: 0.08rem;
    }

    .mini-label {
        color: var(--muted);
        font-size: 0.68rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .mini-value {
        color: var(--text);
        font-size: 1rem;
        font-weight: 800;
    }

    .mini-sub {
        color: var(--muted-2);
        font-size: 0.74rem;
    }

    .mini-pos { color: var(--green); }
    .mini-neg { color: var(--red); }
    .mini-neutral { color: var(--amber); }

    .tab-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.9rem 0.95rem 0.7rem 0.95rem;
        margin-bottom: 0.8rem;
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

    button[role="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        border-radius: 10px !important;
        padding: 0.45rem 0.9rem !important;
        font-weight: 700 !important;
        border: 1px solid transparent !important;
        margin-right: 0.2rem !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        background: #f8fafc !important;
        border: 1px solid var(--border) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        background: white;
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
    }

    .pill-blue { background: #eef4ff; color: #336ad4; border-color: #d8e7ff; }
    .pill-green { background: #ebfbf4; color: #0f9f67; border-color: #d2f5e5; }
    .pill-purple { background: #f4efff; color: #7c4ce0; border-color: #e6dbff; }
    .pill-amber { background: #fff6e8; color: #ca8a04; border-color: #fde7bf; }
    .pill-red { background: #feeff1; color: #d33a4c; border-color: #ffd7dd; }

    .stDownloadButton button,
    .stButton button {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
        background: #ffffff !important;
        color: var(--text) !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    .stTextInput input,
    .stNumberInput input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    div[data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        min-height: 94px;
        box-shadow: none;
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
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.8rem;
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
    """, unsafe_allow_html=True)


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
