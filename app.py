import os
import pandas as pd
import streamlit as st

from services.universe import load_nifty500_universe

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.title("Guru Scanner")
st.caption("Cache-first scanner mode")

price_file = "data/latest_prices.csv"

if not os.path.exists(price_file):
    st.error("No cached price file found. Please generate latest_prices.csv first.")
    st.stop()

if os.path.getsize(price_file) == 0:
    st.error("latest_prices.csv exists but is empty. Please regenerate the file with data.")
    st.stop()

try:
    history = pd.read_csv(price_file)
except pd.errors.EmptyDataError:
    st.error("latest_prices.csv has no valid CSV content. Please regenerate it.")
    st.stop()

st.success(f"Loaded cached price history: {len(history)} rows")

universe = load_nifty500_universe()
st.success(f"Universe loaded: {len(universe)} stocks")

st.subheader("Universe Preview")
st.dataframe(universe.head(10), use_container_width=True, hide_index=True)

st.subheader("Cached Price Preview")
st.dataframe(history.head(20), use_container_width=True, hide_index=True)
