import pandas as pd


def apply_liquidity_filters(
    metrics_df: pd.DataFrame,
    min_price: float = 50.0,
    min_avg_volume_20: float = 100000,
    min_avg_traded_value_20: float = 5_00_00_000,
    enable_filter: bool = True,
):
    if metrics_df.empty:
        return metrics_df.copy(), len(metrics_df), len(metrics_df)

    source_count = len(metrics_df)

    if not enable_filter:
        return metrics_df.copy(), source_count, source_count

    out = metrics_df.copy()

    out = out[
        (out["close"].fillna(0) >= min_price) &
        (out["avg_volume_20"].fillna(0) >= min_avg_volume_20) &
        (out["avg_traded_value_20"].fillna(0) >= min_avg_traded_value_20)
    ].copy()

    filtered_count = len(out)
    return out.reset_index(drop=True), source_count, filtered_count


def get_default_liquidity_profile(universe_mode: str, strict_mode: bool = False):
    if universe_mode == "Nifty 750 (Total Market)":
        if strict_mode:
            return {
                "min_price": 80.0,
                "min_avg_volume_20": 200000,
                "min_avg_traded_value_20": 10_00_00_000,
            }
        return {
            "min_price": 40.0,
            "min_avg_volume_20": 100000,
            "min_avg_traded_value_20": 5_00_00_000,
        }

    if strict_mode:
        return {
            "min_price": 100.0,
            "min_avg_volume_20": 150000,
            "min_avg_traded_value_20": 15_00_00_000,
        }

    return {
        "min_price": 50.0,
        "min_avg_volume_20": 100000,
        "min_avg_traded_value_20": 5_00_00_000,
    }
