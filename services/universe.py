import pandas as pd
import requests
import streamlit as st
from io import StringIO

NIFTY_500_CSV_URL = 'https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv'

@st.cache_data(ttl=86400, show_spinner=False)
def load_nifty500_universe() -> pd.DataFrame:
    response = requests.get(NIFTY_500_CSV_URL, timeout=30)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    cols = {c.lower(): c for c in df.columns}
    symbol_col = cols.get('symbol') or cols.get('ticker') or list(df.columns)[0]
    company_col = cols.get('company name') or cols.get('company_name') or list(df.columns)[1]
    sector_col = cols.get('industry') or cols.get('sector') or list(df.columns)[2]
    out = df[[symbol_col, company_col, sector_col]].copy()
    out.columns = ['symbol', 'company_name', 'sector']
    out['symbol'] = out['symbol'].astype(str).str.replace('.NS', '', regex=False).str.strip()
    out = out.dropna(subset=['symbol']).drop_duplicates(subset=['symbol'])
    return out
