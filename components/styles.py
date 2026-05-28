import streamlit as st

def inject_global_styles():
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(56,189,248,.10), transparent 25%),
            radial-gradient(circle at top left, rgba(16,185,129,.08), transparent 22%),
            linear-gradient(180deg, #071019 0%, #08131d 100%);
    }
    .panel {
        background: rgba(17,24,39,0.72);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 22px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .muted { color:#94a3b8; }
    .title { color:#e5eef9; font-size:1.15rem; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)
