import pandas as pd
import numpy as np

def build_row(meta: dict, df: pd.DataFrame) -> dict:
    x = df.copy()
    x['sma20'] = x['close'].rolling(20).mean()
    x['sma50'] = x['close'].rolling(50).mean()
    x['daily_pct'] = x['close'].pct_change() * 100
    x['weekly_pct'] = x['close'].pct_change(5) * 100
    x['high_126'] = x['close'].rolling(min(126, len(x))).max()
    x['dist_52w_high'] = ((x['high_126'] - x['close']) / x['high_126']) * 100
    x['rs_proxy'] = x['close'].pct_change(min(63, max(2, len(x)-1))) * 100
    x['trend_ok'] = (x['close'] > x['sma20']) & (x['sma20'] > x['sma50'])
    latest = x.dropna().iloc[-1] if not x.dropna().empty else x.iloc[-1]
    badge = 'Trend' if bool(latest.get('trend_ok', False)) else 'Watch'
    return {
        'Symbol': meta['symbol'],
        'Company': meta['company_name'],
        'Sector': meta['sector'],
        'Price': round(float(latest.get('close', 0)), 2),
        'Daily %': round(float(latest.get('daily_pct', 0)), 2),
        'Weekly %': round(float(latest.get('weekly_pct', 0)), 2),
        'RS': round(float(latest.get('rs_proxy', 0)), 2),
        'SMA20': round(float(latest.get('sma20', 0)), 2) if pd.notna(latest.get('sma20', np.nan)) else None,
        'SMA50': round(float(latest.get('sma50', 0)), 2) if pd.notna(latest.get('sma50', np.nan)) else None,
        '52W High Dist': round(float(latest.get('dist_52w_high', 0)), 2),
        'Badge': badge
    }
