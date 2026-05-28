import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    :root {
        --bg: #07111F;
        --bg-soft: #0B1422;
        --panel: rgba(13, 23, 38, 0.78);
        --panel-strong: #0F1B2D;
        --border: rgba(120, 140, 170, 0.18);
        --text: #E8EEF9;
        --muted: #8FA2BF;
        --accent: #00E5A8;
        --accent-2: #23C9FF;
        --gold: #D7B56D;
        --danger: #FF6B6B;
        --warning: #FFB84D;
        --shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
        --radius: 18px;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(35, 201, 255, 0.08), transparent 30%),
            radial-gradient(circle at top right, rgba(0, 229, 168, 0.08), transparent 25%),
            linear-gradient(180deg, #07111F 0%, #081321 55%, #07111F 100%);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1220 0%, #0C1525 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 2rem;
        max-width: 1520px;
    }

    h1, h2, h3, h4 {
        color: var(--text) !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.35rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.1rem !important;
    }

    p, label, div, span {
        color: inherit;
    }

    .app-shell {
        background: linear-gradient(180deg, rgba(7,17,31,0.45), rgba(7,17,31,0.15));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.1rem 1.25rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .hero-bar {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }

    .hero-kicker {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .hero-sub {
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 0.35rem;
    }

    .status-pills {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
    }

    .status-pill {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: 999px;
        padding: 0.5rem 0.85rem;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .status-pill .live-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 8px;
        border-radius: 999px;
        background: var(--accent);
        box-shadow: 0 0 0 5px rgba(0, 229, 168, 0.12);
    }

    .snapshot-card {
        background: linear-gradient(180deg, rgba(16, 27, 44, 0.92), rgba(10, 18, 32, 0.94));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.85rem 1rem;
        box-shadow: var(--shadow);
        min-height: 92px;
    }

    .snapshot-label {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .snapshot-value {
        color: var(--text);
        font-size: 1.6rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .snapshot-sub {
        color: var(--muted);
        font-size: 0.82rem;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, rgba(16, 27, 44, 0.92), rgba(10, 18, 32, 0.94));
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.95rem 1rem;
        box-shadow: var(--shadow);
        min-height: 112px;
    }

    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    .section-card {
        background: linear-gradient(180deg, rgba(13, 23, 38, 0.8), rgba(11, 20, 34, 0.92));
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1rem 1rem 0.35rem 1rem;
        box-shadow: var(--shadow);
        margin-bottom: 0.75rem;
    }

    .section-label {
        color: var(--gold);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .section-title {
        color: var(--text);
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .section-sub {
        color: var(--muted);
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
    }

    .badge-row {
        display: flex;
        gap: 0.45rem;
        flex-wrap: wrap;
        margin-bottom: 0.65rem;
    }

    .badge-chip {
        border-radius: 999px;
        padding: 0.38rem 0.72rem;
        font-size: 0.74rem;
        font-weight: 700;
        border: 1px solid transparent;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    .badge-green {
        background: rgba(0, 229, 168, 0.12);
        color: #8FF7D4;
        border-color: rgba(0, 229, 168, 0.2);
    }

    .badge-blue {
        background: rgba(35, 201, 255, 0.12);
        color: #9DE7FF;
        border-color: rgba(35, 201, 255, 0.2);
    }

    .badge-gold {
        background: rgba(215, 181, 109, 0.14);
        color: #F3D89B;
        border-color: rgba(215, 181, 109, 0.2);
    }

    .badge-red {
        background: rgba(255, 107, 107, 0.14);
        color: #FFC1C1;
        border-color: rgba(255, 107, 107, 0.2);
    }

    button[kind="secondary"],
    .stDownloadButton button,
    .stButton button {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        background: linear-gradient(180deg, rgba(20, 31, 48, 1), rgba(11, 20, 34, 1)) !important;
        color: var(--text) !important;
        font-weight: 700 !important;
    }

    .stDownloadButton button:hover,
    .stButton button:hover {
        border-color: rgba(0, 229, 168, 0.45) !important;
        color: white !important;
        box-shadow: 0 0 0 1px rgba(0,229,168,0.12) inset;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stTextInput input,
    .stNumberInput input {
        background: rgba(10, 18, 32, 0.95) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(0, 229, 168, 0.15) !important;
        border: 1px solid rgba(0, 229, 168, 0.25) !important;
        color: var(--text) !important;
        border-radius: 999px !important;
    }

    button[role="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.75rem 0.95rem !important;
        font-weight: 700 !important;
        border-bottom: 2px solid transparent !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid var(--accent) !important;
        background: rgba(255,255,255,0.02) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 18px;
        overflow: hidden;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }

    div[data-testid="stDataFrame"] [role="grid"] {
        background: rgba(10, 18, 32, 0.92);
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #0F1B2D !important;
        color: #B8C6DA !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: rgba(10, 18, 32, 0.92) !important;
        color: var(--text) !important;
        border-color: rgba(120, 140, 170, 0.08) !important;
    }

    [data-testid="column"] {
        align-self: start;
    }

    .sidebar-title {
        color: var(--text);
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .sidebar-sub {
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 1rem;
    }

    .mini-note {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: -0.2rem;
        margin-bottom: 0.6rem;
    }

    .stCaption {
        color: var(--muted) !important;
    }

    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0 1.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero(universe_mode: str):
    st.markdown(
        f"""
        <div class="app-shell">
            <div class="hero-bar">
                <div class="hero-left">
                    <div class="hero-kicker">Momentum Intelligence Platform</div>
                    <h1>Guru Scanner</h1>
                    <div class="hero-sub">Premium NSE momentum radar with universe filtering, liquidity controls, multi-scanner ranking, and export-ready workflows — currently running in <b>{universe_mode}</b> mode.</div>
                </div>
                <div class="status-pills">
                    <div class="status-pill"><span class="live-dot"></span>Live UI</div>
                    <div class="status-pill">Build Stable</div>
                    <div class="status-pill">Cache-First</div>
                    <div class="status-pill">Scanner Active</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(label: str, title: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-label">{label}</div>
            <div class="section-title">{title}</div>
            <div class="section-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-title">Guru Scanner</div>
        <div class="sidebar-sub">Institutional momentum workspace</div>
        """,
        unsafe_allow_html=True,
    )


def render_snapshot_row(
    universe_count: int,
    post_liquidity_count: int,
    q_count: int,
    m_count: int,
    c_count: int,
):
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")

    cards = [
        ("Universe", f"{universe_count:,}", "Selected constituents"),
        ("Liquid Names", f"{post_liquidity_count:,}", "After liquidity filters"),
        ("Q Scan", f"{q_count:,}", "Qullamaggie matches"),
        ("M Scan", f"{m_count:,}", "Minervini matches"),
        ("Consensus", f"{c_count:,}", "Overlap candidates"),
    ]

    for col, (label, value, sub) in zip([c1, c2, c3, c4, c5], cards):
        with col:
            st.markdown(
                f"""
                <div class="snapshot-card">
                    <div class="snapshot-label">{label}</div>
                    <div class="snapshot-value">{value}</div>
                    <div class="snapshot-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_badge_row():
    st.markdown(
        """
        <div class="badge-row">
            <span class="badge-chip badge-green">Qullamaggie</span>
            <span class="badge-chip badge-blue">Minervini</span>
            <span class="badge-chip badge-gold">Consensus</span>
            <span class="badge-chip badge-red">High Risk If Illiquid</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
