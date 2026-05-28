import math
import pandas as pd
import streamlit as st
import yfinance as yf

def _chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

@st.cache_data(ttl=60 * 60 * 6, show_spinner=False)
def fetch_history(symbols, period="1y", interval="1d", batch_size=50):
    all_frames = []

    for batch in _chunk_list(symbols, batch_size):
        try:
            df = yf.download(
                tickers=batch,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False,
                group_by="ticker",
                threads=True,
                timeout=20,
            )

            if df is None or df.empty:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                batch_frames = []
                for ticker in batch:
                    if ticker in df.columns.get_level_values(0):
                        one = df[ticker].copy()
                        one["yf_symbol"] = ticker
                        one = one.reset_index()
                        batch_frames.append(one)

                if batch_frames:
                    all_frames.append(pd.concat(batch_frames, ignore_index=True))
            else:
                one = df.copy().reset_index()
                one["yf_symbol"] = batch[0]
                all_frames.append(one)

        except Exception:
            continue

    if not all_frames:
        return pd.DataFrame()

    out = pd.concat(all_frames, ignore_index=True)
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out
