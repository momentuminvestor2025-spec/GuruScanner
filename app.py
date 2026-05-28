import streamlit as st
from components.styles import (
    inject_global_styles,
    render_hero_header,
    render_scanner_kpi_strip,
    render_sector_heatmap,
)

st.set_page_config(page_title="Momentum Scanner", layout="wide")
inject_global_styles()

render_hero_header()
render_scanner_kpi_strip()
render_sector_heatmap()

st.caption("Static Phase 1 mock page for Momentum Scanner UI")
