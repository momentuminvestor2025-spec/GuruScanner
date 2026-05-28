import pandas as pd


def _normalize_symbol(value: str) -> str:
    if pd.isna(value):
        return ""
    value = str(value).strip().upper()
    if value.endswith(".NS"):
        value = value[:-3]
    return (
        value
        .replace("&", "")
        .replace("-", "")
        .replace(" ", "")
    )


def filter_to_selected_universe(price_df: pd.DataFrame, universe_df: pd.DataFrame):
    if price_df.empty:
        return price_df.copy(), 0, 0

    df = price_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    if "yf_symbol" not in df.columns:
        raise ValueError("latest_prices.csv must contain a yf_symbol column")

    df["yf_symbol"] = df["yf_symbol"].astype(str).str.strip().str.upper()
    df["symbol_key"] = df["yf_symbol"].map(_normalize_symbol)

    u = universe_df.copy()
    u["yf_symbol"] = u["yf_symbol"].astype(str).str.strip().str.upper()
    u["symbol_key"] = u["yf_symbol"].map(_normalize_symbol)

    universe_keys = set(u["symbol_key"].dropna().unique().tolist())

    total_source_rows = len(df)
    filtered = df[df["symbol_key"].isin(universe_keys)].copy()
    total_filtered_rows = len(filtered)

    return filtered.reset_index(drop=True), total_source_rows, total_filtered_rows
