import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(39, 83, 255, 0.10), transparent 18%),
            radial-gradient(circle at top right, rgba(0, 255, 170, 0.05), transparent 12%),
            linear-gradient(180deg, #040816 0%, #06101f 55%, #07111d 100%);
        color: #e5edf7;
    }

    .block-container {
        max-width: 1560px;
        padding-top: 0.55rem;
        padding-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(8, 14, 28, 0.92);
        border-right: 1px solid rgba(120, 145, 190, 0.10);
    }

    .hero-shell, .sector-heatmap-shell {
        position: relative;
        overflow: hidden;
        border-radius: 18px;
        background:
            radial-gradient(circle at top left, rgba(255,255,255,0.04), transparent 24%),
            linear-gradient(145deg, #07101d 0%, #081523 52%, #06111d 100%);
        border: 1px solid rgba(88, 112, 153, 0.16);
        box-shadow:
            0 18px 36px rgba(0,0,0,0.20),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .hero-shell::after,
    .sector-heatmap-shell::after,
    .scanner-kpi-card::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent 20%);
    }

    .hero-shell {
        padding: 14px 14px 10px 14px;
        margin-bottom: 0.9rem;
    }

    .hero-top {
        display: grid;
        grid-template-columns: 1.25fr 1fr auto;
        gap: 14px;
        align-items: center;
    }

    .hero-brand-title {
        font-size: 1.08rem;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #f8fbff;
    }

    .hero-brand-title .accent {
        color: #1de982;
    }

    .hero-brand-sub {
        margin-top: 4px;
        color: rgba(205, 218, 235, 0.72);
        font-size: 0.80rem;
    }

    .hero-search {
        height: 46px;
        border-radius: 13px;
        padding: 0 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(18, 26, 45, 0.88);
        border: 1px solid rgba(120, 145, 190, 0.12);
        color: rgba(225, 233, 245, 0.92);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .hero-search-text {
        color: rgba(205, 218, 235, 0.58);
        font-size: 0.88rem;
        flex: 1;
    }

    .hero-kbd {
        border-radius: 8px;
        padding: 3px 8px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.05);
        color: rgba(205, 218, 235, 0.52);
        font-size: 0.72rem;
        font-weight: 700;
    }

    .hero-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-btn {
        height: 46px;
        border-radius: 13px;
        padding: 0 16px;
        display: inline-flex;
        align-items: center;
        gap: 9px;
        background: rgba(18, 26, 45, 0.92);
        border: 1px solid rgba(120, 145, 190, 0.12);
        color: #e9f1fb;
        font-size: 0.86rem;
        font-weight: 600;
    }

    .hero-icon-btn {
        width: 46px;
        justify-content: center;
        padding: 0;
    }

    .hero-time {
        margin-left: 6px;
        text-align: right;
        white-space: nowrap;
    }

    .hero-time-status {
        color: #ff6b6b;
        font-size: 0.84rem;
        font-weight: 700;
    }

    .hero-time-date {
        margin-top: 4px;
        color: rgba(205, 218, 235, 0.72);
        font-size: 0.79rem;
    }

    .breadth-strip {
        margin-top: 14px;
        border-radius: 16px;
        padding: 12px 10px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)), rgba(6, 13, 26, 0.72);
        border: 1px solid rgba(120, 145, 190, 0.10);
        display: grid;
        grid-template-columns: 1.05fr repeat(8, 1fr);
    }

    .breadth-item {
        padding: 0 14px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 52px;
        border-right: 1px solid rgba(120, 145, 190, 0.10);
    }

    .breadth-item:last-child {
        border-right: none;
    }

    .breadth-label {
        color: rgba(205, 218, 235, 0.70);
        font-size: 0.74rem;
        margin-bottom: 5px;
        font-weight: 600;
    }

    .breadth-value {
        color: #f8fbff;
        font-size: 0.98rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .breadth-sub {
        color: rgba(205, 218, 235, 0.80);
        font-size: 0.77rem;
        margin-top: 2px;
    }

    .green { color: #1de982 !important; }
    .red { color: #ff6b6b !important; }

    .scanner-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 0.1rem 0 0.9rem;
    }

    .scanner-kpi-card {
        position: relative;
        overflow: hidden;
        min-height: 122px;
        border-radius: 16px;
        padding: 14px 14px 12px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: radial-gradient(circle at top left, rgba(255,255,255,0.05), transparent 26%), linear-gradient(145deg, #07101d 0%, #081523 55%, #06111d 100%);
        border: 1px solid rgba(88, 112, 153, 0.16);
        box-shadow: 0 16px 30px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .scanner-kpi-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
        position: relative;
        z-index: 1;
    }

    .scanner-kpi-icon {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        font-weight: 700;
        flex: 0 0 auto;
        background: rgba(255,255,255,0.03);
    }

    .scanner-kpi-label {
        color: rgba(215, 225, 240, 0.76);
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
        margin-bottom: 7px;
        white-space: nowrap;
    }

    .scanner-kpi-value {
        color: #f8fbff;
        font-size: 1.95rem;
        line-height: 1;
        font-weight: 800;
        margin-bottom: 7px;
        letter-spacing: -0.03em;
    }

    .scanner-kpi-delta {
        font-size: 0.80rem;
        font-weight: 600;
    }

    .scanner-kpi-right {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: flex-end;
        justify-content: flex-end;
        min-width: 72px;
    }

    .scanner-sparkline {
        width: 72px;
        height: 26px;
        opacity: 0.95;
    }

    .scanner-green .scanner-kpi-icon {
        color: #20e38b;
        border: 1px solid rgba(32,227,139,0.50);
        box-shadow: 0 0 0 3px rgba(32,227,139,0.06);
    }
    .scanner-green .scanner-kpi-delta { color: #20e38b; }

    .scanner-cyan .scanner-kpi-icon {
        color: #1ed7ff;
        border: 1px solid rgba(30,215,255,0.50);
        box-shadow: 0 0 0 3px rgba(30,215,255,0.06);
    }
    .scanner-cyan .scanner-kpi-delta { color: #1ed7ff; }

    .scanner-gold .scanner-kpi-icon {
        color: #f4b942;
        border: 1px solid rgba(244,185,66,0.50);
        box-shadow: 0 0 0 3px rgba(244,185,66,0.06);
    }
    .scanner-gold .scanner-kpi-delta { color: #f4b942; }

    .scanner-purple .scanner-kpi-icon {
        color: #8b5cff;
        border: 1px solid rgba(139,92,255,0.50);
        box-shadow: 0 0 0 3px rgba(139,92,255,0.06);
    }
    .scanner-purple .scanner-kpi-delta { color: #8b5cff; }

    .sector-heatmap-shell {
        padding: 12px 12px 10px 12px;
        margin-bottom: 1rem;
    }

    .sector-heatmap-head {
        position: relative;
        z-index: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }

    .sector-heatmap-title {
        color: #f8fbff;
        font-size: 0.92rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .sector-heatmap-title .muted {
        color: rgba(205,218,235,0.55);
        font-weight: 700;
        margin-left: 6px;
    }

    .sector-heatmap-filter {
        border-radius: 12px;
        padding: 7px 12px;
        background: rgba(18, 26, 45, 0.86);
        border: 1px solid rgba(120, 145, 190, 0.10);
        color: rgba(225,233,245,0.76);
        font-size: 0.80rem;
        font-weight: 600;
        white-space: nowrap;
    }

    .sector-grid {
        position: relative;
        z-index: 1;
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 2px;
        border-radius: 14px;
        overflow: hidden;
        background: rgba(255,255,255,0.03);
    }

    .sector-tile {
        min-height: 86px;
        padding: 12px 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .sector-name {
        color: #f8fbff;
        font-size: 0.82rem;
        font-weight: 700;
        line-height: 1.15;
        margin-bottom: 8px;
        max-width: 92%;
    }

    .sector-score {
        color: #ffffff;
        font-size: 1.45rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }

    .sector-change {
        font-size: 0.90rem;
        font-weight: 700;
    }

    .heat-green-5 { background: linear-gradient(180deg, #0f4732 0%, #0d3c2b 100%); }
    .heat-green-4 { background: linear-gradient(180deg, #0d3e2c 0%, #0b3425 100%); }
    .heat-green-3 { background: linear-gradient(180deg, #0b3526 0%, #092c20 100%); }
    .heat-green-2 { background: linear-gradient(180deg, #0a2d21 0%, #08251b 100%); }
    .heat-green-1 { background: linear-gradient(180deg, #08241b 0%, #071c15 100%); }

    .heat-red-1 { background: linear-gradient(180deg, #241016 0%, #1c0c11 100%); }
    .heat-red-2 { background: linear-gradient(180
