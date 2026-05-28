import pandas as pd
import yfinance as yf

def fetch_one_symbol_debug(symbol, period="6mo", interval="1d"):
    try:
        df = yf.download(
            tickers=symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            threads=False,
            timeout=30,
        )

        if df is None:
            return {"ok": False, "reason": "yf.download returned None", "data": pd.DataFrame()}

        if df.empty:
            return {"ok": False, "reason": "yf.download returned empty dataframe", "data": pd.DataFrame()}

        out = df.copy().reset_index()
        out["yf_symbol"] = symbol
        out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
        return {"ok": True, "reason": "success", "data": out}

    except Exception as e:
        return {"ok": False, "reason": str(e), "data": pd.DataFrame()}
