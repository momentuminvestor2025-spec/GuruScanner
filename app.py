import streamlit as st
import pandas as pd
from components.styles import inject_global_styles
from services.universe import load_nifty500_universe
from services.market_data import fetch_history
from services.indicators import build_row

st.set_page_config(page_title='Guru Scanner', page_icon='📈', layout='wide')
inject_global_styles()

st.title('Guru Scanner')
st.caption('Nifty 500 universe loader with Yahoo Finance data and scanner filters.')

with st.sidebar:
    st.markdown('## Navigation')
    page = st.radio('Go to', ['Dashboard', 'Qullamaggie', 'Minervini', "O'Neil", 'Consensus', 'Backtesting', 'Alerts', 'Admin'])
    universe_limit = st.slider('Universe batch size', 20, 200, 60, 10)
    min_price = st.number_input('Minimum price', value=100.0)
    min_rs = st.number_input('Minimum RS', value=0.0)
    max_dist = st.number_input('Max 52W High Distance', value=25.0)
    trend_only = st.checkbox('Trend filter only', value=False)
    refresh = st.button('Refresh data')

if refresh:
    st.cache_data.clear()

with st.spinner('Loading Nifty 500 universe...'):
    universe = load_nifty500_universe()

universe = universe.head(universe_limit)
rows = []
with st.spinner('Fetching Yahoo Finance data...'):
    for _, meta in universe.iterrows():
        try:
            hist = fetch_history(meta['symbol'])
            if hist.empty:
                continue
            rows.append(build_row(meta.to_dict(), hist))
        except Exception:
            continue

df = pd.DataFrame(rows)
if not df.empty:
    filtered = df.copy()
    filtered = filtered[filtered['Price'] >= min_price]
    filtered = filtered[filtered['RS'] >= min_rs]
    filtered = filtered[filtered['52W High Dist'] <= max_dist]
    if trend_only:
        filtered = filtered[filtered['Badge'] == 'Trend']
else:
    filtered = df

c1, c2, c3, c4 = st.columns(4)
metrics = [
    ('Universe Loaded', str(len(universe))),
    ('Visible Rows', str(len(filtered)) if not filtered.empty else '0'),
    ('Data Source', 'Nifty CSV + Yahoo'),
    ('Active View', page),
]
for col, (label, value) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(f"<div class='panel'><div class='muted'>{label}</div><div class='title'>{value}</div></div>", unsafe_allow_html=True)

left, right = st.columns([1.7, 1])
with left:
    st.markdown(f"<div class='panel'><div class='title'>{page} Scanner</div><div class='muted'>Rows are filtered from the Nifty 500 constituent universe using Yahoo Finance daily data.</div></div>", unsafe_allow_html=True)
    search = st.text_input('Search symbol or company')
    table_df = filtered.copy()
    if not table_df.empty and search:
        table_df = table_df[
            table_df['Symbol'].str.contains(search, case=False, na=False) |
            table_df['Company'].str.contains(search, case=False, na=False)
        ]
    st.dataframe(table_df, use_container_width=True, height=520)

with right:
    sectors = filtered['Sector'].value_counts().head(10).to_frame('Count') if not filtered.empty else pd.DataFrame(columns=['Count'])
    st.markdown("<div class='panel'><div class='title'>Sector Snapshot</div><div class='muted'>Top sectors among visible filtered rows.</div></div>", unsafe_allow_html=True)
    st.dataframe(sectors, use_container_width=True, height=240)
    st.markdown("<div class='panel'><div class='title'>Deployment Check</div><div class='muted'>If you can see filtered Nifty 500 rows, your universe loader and Yahoo integration are working.</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'><div class='title'>Next Step</div><div class='muted'>Add full scanner methodologies, historical storage, alerts, and detailed stock pages next.</div></div>", unsafe_allow_html=True)
