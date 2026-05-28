import streamlit as st
from services.universe import load_nifty500_universe
from services.market_data import fetch_one_symbol_debug

st.set_page_config(page_title="Guru Scanner", layout="wide")

st.title("Guru Scanner")
st.caption("Yahoo debug mode")

universe = load_nifty500_universe()
st.success(f"Universe loaded: {len(universe)} stocks")

st.subheader("Universe Preview")
st.dataframe(universe.head(10), use_container_width=True, hide_index=True)

test_symbol = st.text_input("Test Yahoo symbol", value="ABB.NS")

result = fetch_one_symbol_debug(test_symbol)

st.write("Debug status:", result["ok"])
st.write("Debug reason:", result["reason"])

if result["ok"]:
    st.success(f"Fetched {len(result['data'])} rows for {test_symbol}")
    st.dataframe(result["data"].head(20), use_container_width=True, hide_index=True)
else:
    st.error("Yahoo fetch failed")
