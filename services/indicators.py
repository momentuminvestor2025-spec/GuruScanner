import numpy as np
import pandas as pd

def compute_metrics(price_df, universe_df):
    if price_df.empty:
        return pd.DataFrame()

    df = price_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["yf_symbol", "date"]).reset_index(drop=True)

    grouped = df.groupby("yf_symbol", group_keys=False)

    df["ema10"] = grouped["close"].transform(lambda s: s.ewm(span=10, adjust=False).mean())
    df["sma20"] = grouped["close"].transform(lambda s: s.rolling(20).mean())
    df["sma50"] = grouped["close"].transform(lambda s: s.rolling(50).mean())
    df["sma100"] = grouped["close"].transform(lambda s: s.rolling(100).mean())
    df["sma200"] = grouped["close"].transform(lambda s: s.rolling(200).mean())

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

    df["high_252"] = grouped["high"].transform(lambda s: s.rolling(252).max())
    df["low_20"] = grouped["low"].transform(lambda s: s.rolling(20).min())
    df["high_20"] = grouped["high"].transform(lambda s: s.rolling(20).max())

    df["dist_52w_high_pct"] = ((df["high_252"] - df["close"]) / df["high_252"]) * 100
    df["range_pos_20"] = ((df["close"] - df["low_20"]) / (df["high_20"] - df["low_20"])) * 100

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["prev_close"]).abs()
    tr3 = (df["low"] - df["prev_close"]).abs()
    df["true_range"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df["atr_14"] = grouped["true_range"].transform(lambda s: s.rolling(14).mean())

    df["avg_volume_20"] = grouped["volume"].transform(lambda s: s.rolling(20).mean())
    df["volume_surge"] = df["volume"] / df["avg_volume_20"]

    latest = df.groupby("yf_symbol").tail(1).copy()

    latest["rs_raw"] = (
        latest["ret_1m"].fillna(0) * 0.25 +
        latest["ret_3m"].fillna(0) * 0.35 +
        latest["ret_6m"].fillna(0) * 0.40
    )

    latest["atr_rs_raw"] = latest["atr_14"].rank(pct=True) * 100
    latest["rs_score"] = latest["rs_raw"].rank(pct=True) * 100

    out = latest.merge(
        universe_df[["symbol", "company", "sector", "yf_symbol"]],
        on="yf_symbol",
        how="left"
    )

    cols = [
        "symbol", "company", "sector", "yf_symbol", "date", "close", "daily_pct", "weekly_pct",
        "ema10", "sma20", "sma50", "sma100", "sma200",
        "ret_1m", "ret_3m", "ret_6m", "ret_12m",
        "high_252", "dist_52w_high_pct", "range_pos_20",
        "atr_14", "atr_rs_raw", "avg_volume_20", "volume_surge", "rs_score"
    ]

    out = out[cols].sort_values("rs_score", ascending=False).reset_index(drop=True)
    return out
