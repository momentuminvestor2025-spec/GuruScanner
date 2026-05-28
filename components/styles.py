import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    :root {
        --bg: #08111d;
        --panel: #0d1726;
        --panel-2: #101c2e;
        --border: rgba(148, 163, 184, 0.16);
        --text: #e5edf7;
        --muted: #94a3b8;

        --green: #16c784;
        --blue: #3b82f6;
        --gold: #f59e0b;
        --purple: #8b5cf6;
        --red: #ef4444;
    }

    .stApp {
        background: #08111d;
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #0b1524;
        border-right: 1px solid var(--border);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.02em;
    }

    .app-header {
        background: #0c1626;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }

    .app-kicker {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .app-subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }

    .color-card {
        border-radius: 18px;
        padding: 0.9rem 1rem;
        color: white;
        min-height: 96px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: none;
    }

    .card-green { background: linear-gradient(180deg, #123b30 0%, #0f2f27 100%); }
    .card-blue { background: linear-gradient(180deg, #142f5a 0%, #112746 100%); }
    .card-gold { background: linear-gradient(180deg, #4b3411 0%, #3a280d 100%); }
    .card-purple { background: linear-gradient(180deg, #35204f 0%, #2b1a40 100%); }

    .color-card-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.82;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .color-card-value {
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .color-card-sub {
        font-size: 0.82rem;
        opacity: 0.82;
    }

    .section-box {
        background: #0c1626;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.95rem 1rem 0.6rem 1rem;
        margin-bottom: 0.9rem;
    }

    .section-label {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .section-title {
        color: var(--text);
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .section-sub {
        color: var(--muted);
        font-size: 0.88rem;
        margin-bottom: 0.65rem;
    }

    div[data-testid="metric-container"] {
        background: #0f1b2d;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
        min-height: 102px;
        box-shadow: none;
    }

    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
    }

    button[role="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 0.75rem 1rem !important;
        font-weight: 700 !important;
        border-bottom: 2px solid transparent !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid #16c784 !important;
        background: rgba(255,255,255,0.02) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 1rem;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #0f1b2d !important;
        color: #aebed3 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: #0b1524 !important;
        color: var(--text) !important;
        border-color: rgba(148, 163, 184, 0.08) !important;
    }

    .sidebar-brand {
        color: var(--text);
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .sidebar-sub {
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 1rem;
    }

    .scanner-pill-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 0.8rem;
    }

    .scanner-pill {
        border-radius: 999px;
        padding: 0.38rem 0.72rem;
        font-size: 0.74rem;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .pill-green { background: rgba(22, 199, 132, 0.12); color: #7ef0bd; }
    .pill-blue { background: rgba(59, 130, 246, 0.12); color: #93c5fd; }
    .pill-gold { background: rgba(245, 158, 11, 0.14); color: #fcd34d; }
    .pill-purple { background: rgba(139, 92, 246, 0.14); color: #c4b5fd; }

    .stDownloadButton button,
    .stButton button {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        background: #101c2e !important;
        color: var(--text) !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    .stTextInput input,
    .stNumberInput input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #0b1524 !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-brand">Guru Scanner</div>
        <div class="sidebar-sub">Clean institutional scanner workspace</div>
        """,
        unsafe_allow_html=True,
    )


def render_header(universe_mode: str):
    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-kicker">Momentum Scanner</div>
            <h1>Guru Scanner</h1>
            <div class="app-subtitle">Liquidity-aware NSE scanner running in <b>{universe_mode}</b> mode.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_box(label: str, title: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="section-box">
            <div class="section-label">{label}</div>
            <div class="section-title">{title}</div>
            <div class="section-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_color_kpis(universe_count: int, liquid_count: int, q_count: int, m_count: int):
    c1, c2, c3, c4 = st.columns(4, gap="small")
    cards = [
        ("Universe", f"{universe_count:,}", "Selected constituents", "card-green"),
        ("Liquid", f"{liquid_count:,}", "After liquidity filters", "card-blue"),
        ("Qullamaggie", f"{q_count:,}", "Q scanner matches", "card-gold"),
        ("Minervini", f"{m_count:,}", "M scanner matches", "card-purple"),
    ]

    for col, (label, value, sub, cls) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="color-card {cls}">
                    <div class="color-card-label">{label}</div>
                    <div class="color-card-value">{value}</div>
                    <div class="color-card-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_scanner_pills():
    st.markdown(
        """
        <div class="scanner-pill-row">
            <span class="scanner-pill pill-green">Qullamaggie</span>
            <span class="scanner-pill pill-blue">Minervini</span>
            <span class="scanner-pill pill-gold">Consensus</span>
            <span class="scanner-pill pill-purple">Metrics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
