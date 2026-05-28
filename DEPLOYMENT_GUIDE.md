# Step-by-Step Deployment Guide

## 1. Download and extract
Download the ZIP and extract it locally.

## 2. Create a new GitHub repo
Create a fresh GitHub repository and upload all extracted files.

## 3. Confirm root structure
Make sure these files exist at the repo root:
- `app.py`
- `requirements.txt`
- `packages.txt`
- `.streamlit/config.toml`
- `components/`
- `services/`

## 4. Important checks
- `app.py` must start with Python code
- `.streamlit/config.toml` must contain the theme block
- `packages.txt` must remain empty

## 5. Deploy on Streamlit Community Cloud
- Click **Create app**
- Select repo and `main` branch
- Main file path: `app.py`
- Deploy

## 6. First load expectations
- The app downloads the Nifty 500 constituent CSV
- Then it pulls Yahoo Finance data for a limited batch size first
- Use filters to inspect results

## 7. If rows are slow
- Reduce the universe limit from the sidebar
- Click refresh once
- Reboot app if Yahoo temporarily blocks or slows requests
