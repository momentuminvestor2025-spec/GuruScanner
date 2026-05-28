import pandas as pd


def run_qullamaggie_screen(metrics_df: pd.DataFrame) -> pd.DataFrame:
    if metrics_df.empty:
        return pd.DataFrame()

    df = metrics_df.copy()

    screened = df[
        (df["rs_score"] >= 50) &
        (df["atr_rs"] >= 50) &
        (df["range_pos_20"] >= 50) &
        (df["ma_aligned"] == True)
    ].copy()

    screened["badge"] = "Q"
    screened["scanner"] = "Qullamaggie"

    screened = screened.sort_values(
        ["rs_score", "atr_rs", "dist_52w_high_pct"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    return screened


def run_minervini_screen(metrics_df: pd.DataFrame) -> pd.DataFrame:
    if metrics_df.empty:
        return pd.DataFrame()

    df = metrics_df.copy()

    # Relaxed early thresholds so the pipeline can be validated
    screened = df[
        (df["close"] > df["sma50"]) &
        (df["close"] > df["sma100"]) &
        (df["sma50"] >= df["sma100"]) &
        (df["green_day"] == True) &
        (df["near_high"] == True) &
        (df["rs_score"] >= 40)
    ].copy()

    screened["badge"] = "M"
    screened["scanner"] = "Minervini"

    screened = screened.sort_values(
        ["rs_score", "dist_52w_high_pct", "volume_surge"],
        ascending=[False, True, False]
    ).reset_index(drop=True)

    return screened


def run_consensus_screen(q_df: pd.DataFrame, m_df: pd.DataFrame) -> pd.DataFrame:
    frames = []

    if not q_df.empty:
        frames.append(q_df[["symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
                            "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
                            "volume_surge", "badge"]])

    if not m_df.empty:
        frames.append(m_df[["symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
                            "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20",
                            "volume_surge", "badge"]])

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    consensus = (
        combined.groupby(
            ["symbol", "company", "sector", "close", "daily_pct", "weekly_pct",
             "rs_score", "atr_rs", "dist_52w_high_pct", "range_pos_20", "volume_surge"],
            dropna=False
        )["badge"]
        .agg(lambda x: "".join(sorted(set(x))))
        .reset_index()
    )

    consensus["scanner_count"] = consensus["badge"].str.len()
    consensus = consensus[consensus["scanner_count"] >= 2].copy()

    consensus = consensus.sort_values(
        ["scanner_count", "rs_score", "dist_52w_high_pct"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    return consensus
