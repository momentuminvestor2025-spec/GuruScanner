import pandas as pd
import streamlit as st
import yfinance as yf

def _chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

@st.cache_data(ttl=60 * 60 * 4, show_spinner=False)
def fetch_history(symbols, period="6mo", interval="1d", batch_size=5):
    all_frames = []

    for batch in _chunk_list(symbols, batch_size):
        try:
            for ticker in batch:
                df = yf.download(
                    tickers=ticker,
                    period=period,
                    interval=interval,
                    auto_adjust=True,
                    progress=False,
                    threads=False,
                    timeout=20,
                )

                if df is None or df.empty:
                    continue

                one = df.copy().reset_index()
                one["yf_symbol"] = ticker
                all_frames.append(one)

        except Exception:
            continue

    if not all_frames:
        return pd.DataFrame()

    out = pd.concat(all_frames, ignore_index=True)
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]

    rename_map = {
        "adj_close": "adj_close",
        "close": "close",
        "high": "high",
        "low": "low",
        "open": "open",
        "volume": "volume",
        "date": "date",
    }
    out = out.rename(columns=rename_map)

    required = {"date", "open", "high", "low", "close", "volume", "yf_symbol"}
    if not required.issubset(set(out.columns)):
        return pd.DataFrame()

    return out
