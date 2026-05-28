import numpy as np
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


def compute_metrics(price_df: pd.DataFrame, universe_df: pd.DataFrame) -> pd.DataFrame:
    if price_df.empty:
        return pd.DataFrame()

    df = price_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = {"date", "open", "high", "low", "close", "volume", "yf_symbol"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in price file: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["yf_symbol"] = df["yf_symbol"].astype(str).str.strip().str.upper()
    df["symbol_key"] = df["yf_symbol"].map(_normalize_symbol)

    u = universe_df.copy()
    u["yf_symbol"] = u["yf_symbol"].astype(str).str.strip().str.upper()
    u["symbol_key"] = u["yf_symbol"].map(_normalize_symbol)

    df = df.dropna(subset=["date", "close", "yf_symbol"]).copy()
    df = df.sort_values(["yf_symbol", "date"]).reset_index(drop=True)

    grouped = df.groupby("yf_symbol", group_keys=False)

    df["ema10"] = grouped["close"].transform(lambda s: s.ewm(span=10, adjust=False).mean())
    df["sma20"] = grouped["close"].transform(lambda s: s.rolling(20, min_periods=1).mean())
    df["sma50"] = grouped["close"].transform(lambda s: s.rolling(50, min_periods=1).mean())
    df["sma100"] = grouped["close"].transform(lambda s: s.rolling(100, min_periods=1).mean())
    df["sma200"] = grouped["close"].transform(lambda s: s.rolling(200, min_periods=1).mean())

    df["prev_close"] = grouped["close"].shift(1)
    df["close_5d"] = grouped["close"].shift(5)
    df["close_21d"] = grouped["close"].shift(21)
    df["close_63d"] = grouped["close"].shift(63)
    df["close_126d"] = grouped["close"].shift(126)
    df["close_252d"] = grouped["close"].shift(252)

    df["daily_pct"] = ((df["close"] / df["prev_close"]) - 1.0) * 100
    df["weekly_pct"] = ((df["close"] / df["close_5d"]) - 1.0) * 100
    df["ret_1m"] = ((df["close"] / df["close_21d"]) - 1.0) * 100
    df["ret_3m"] = ((df["close"] / df["close_63d"]) - 1.0) * 100
    df["ret_6m"] = ((df["close"] / df["close_126d"]) - 1.0) * 100
    df["ret_12m"] = ((df["close"] / df["close_252d"]) - 1.0) * 100

    df["high_252"] = grouped["high"].transform(lambda s: s.rolling(252, min_periods=1).max())
    df["low_20"] = grouped["low"].transform(lambda s: s.rolling(20, min_periods=1).min())
    df["high_20"] = grouped["high"].transform(lambda s: s.rolling(20, min_periods=1).max())

    df["dist_52w_high_pct"] = np.where(
        df["high_252"] > 0,
        ((df["high_252"] - df["close"]) / df["high_252"]) * 100,
        np.nan,
    )

    df["range_pos_20"] = np.where(
        (df["high_20"] - df["low_20"]) > 0,
        ((df["close"] - df["low_20"]) / (df["high_20"] - df["low_20"])) * 100,
        np.nan,
    )

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["prev_close"]).abs()
    tr3 = (df["low"] - df["prev_close"]).abs()
    df["true_range"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df["atr_14"] = grouped["true_range"].transform(lambda s: s.rolling(14, min_periods=1).mean())

    df["traded_value"] = df["close"] * df["volume"]
    df["avg_volume_20"] = grouped["volume"].transform(lambda s: s.rolling(20, min_periods=1).mean())
    df["avg_traded_value_20"] = grouped["traded_value"].transform(lambda s: s.rolling(20, min_periods=1).mean())
    df["volume_surge"] = np.where(df["avg_volume_20"] > 0, df["volume"] / df["avg_volume_20"], np.nan)

    latest = df.groupby("yf_symbol").tail(1).copy()

    latest["rs_raw"] = (
        latest["ret_1m"].fillna(0) * 0.25
        + latest["ret_3m"].fillna(0) * 0.35
        + latest["ret_6m"].fillna(0) * 0.40
    )
    latest["rs_score"] = latest["rs_raw"].rank(pct=True) * 100
    latest["atr_rs"] = latest["atr_14"].rank(pct=True) * 100

    latest = latest.merge(
        u[["symbol_key", "symbol", "company", "sector"]],
        on="symbol_key",
        how="left"
    )

    latest["symbol"] = latest["symbol"].fillna(latest["symbol_key"])
    latest["company"] = latest["company"].fillna("Unknown Company")
    latest["sector"] = latest["sector"].fillna("Unknown Sector")

    latest["ma_aligned"] = (
        (latest["close"] >= latest["ema10"]) &
        (latest["ema10"] >= latest["sma20"]) &
        (latest["sma20"] >= latest["sma50"]) &
        (latest["sma50"] >= latest["sma100"]) &
        (latest["sma100"] >= latest["sma200"])
    )

    latest["near_high"] = latest["dist_52w_high_pct"] <= 25
    latest["green_day"] = latest["daily_pct"].fillna(-999) >= 0

    ordered_cols = [
        "date", "symbol", "company", "sector", "yf_symbol",
        "open", "high", "low", "close", "volume", "traded_value",
        "avg_volume_20", "avg_traded_value_20",
        "daily_pct", "weekly_pct",
        "ret_1m", "ret_3m", "ret_6m", "ret_12m",
        "ema10", "sma20", "sma50", "sma100", "sma200",
        "atr_14", "atr_rs", "volume_surge",
        "high_252", "dist_52w_high_pct", "range_pos_20",
        "rs_raw", "rs_score", "ma_aligned", "near_high", "green_day"
    ]

    return latest[ordered_cols].sort_values("rs_score", ascending=False).reset_index(drop=True)
