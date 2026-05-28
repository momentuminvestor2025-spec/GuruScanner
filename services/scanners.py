import pandas as pd


def run_qullamaggie_screen(metrics_df: pd.DataFrame) -> pd.DataFrame:
    if metrics_df.empty:
        return pd.DataFrame()

    df = metrics_df.copy()

    # Relaxed thresholds for early testing on small cached sample data.
    # Tighten these later when you have 6-12 months of data for the full universe.
    screened = df[
        (df["rs_score"] >= 50) &
        (df["atr_rs"] >= 50) &
        (df["range_pos_20"] >= 50) &
        (df["ma_aligned"] == True)
    ].copy()

    screened["badge"] = "Q"
    screened = screened.sort_values(
        ["rs_score", "atr_rs", "dist_52w_high_pct"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    return screened