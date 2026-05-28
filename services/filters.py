import pandas as pd


def apply_table_filters(df: pd.DataFrame, search_text: str = "", sectors=None) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    if search_text:
        text = search_text.strip().lower()
        out = out[
            out["symbol"].astype(str).str.lower().str.contains(text, na=False) |
            out["company"].astype(str).str.lower().str.contains(text, na=False)
        ]

    if sectors:
        out = out[out["sector"].isin(sectors)]

    return out.reset_index(drop=True)
