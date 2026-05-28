# Guru Scanner - Nifty 500 Loader + Filters

This build upgrades the Yahoo live starter to:
- load the Nifty 500 constituent list from the official Nifty Indices CSV URL
- fetch NSE data from Yahoo Finance using `.NS` tickers
- calculate visible table metrics
- allow scanner-style filtering in the UI

## Notes
- Constituents are loaded from the Nifty Indices CSV list.
- Streamlit runs from repo root on Community Cloud, so all paths are kept deployment-safe.
- First load may take time depending on Yahoo response speed.
