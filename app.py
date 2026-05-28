with right:
    section_header(
        "Controls",
        "Liquidity Rules",
        "Current execution-quality guardrails applied before scanners run."
    )
    st.write(f"**Min Price:** {min_price:,.2f}")
    st.write(f"**Min 20D Avg Volume:** {int(min_avg_volume_20):,}")
    st.write(f"**Min 20D Avg Traded Value:** {int(min_avg_traded_value_20):,}")
    st.write(f"**Search Universe:** {universe_mode}")
    st.write(f"**Strict Liquidity:** {'On' if strict_liquidity else 'Off'}")

    section_header(
        "Leaders",
        "Top RS Names",
        "Highest relative-strength stocks surviving all active filters."
    )

    leader_cols = [
        "symbol", "close", "rs_score", "dist_52w_high_pct",
        "avg_traded_value_20", "volume_surge"
    ]

    if leaders.empty:
        st.info("No leaders available after current filters.")
    else:
        st.dataframe(
            leaders[leader_cols].round(2),
            use_container_width=True,
            hide_index=True,
            column_config={
                "close": st.column_config.NumberColumn("Price", format="%.2f"),
                "rs_score": st.column_config.NumberColumn("RS", format="%.2f"),
                "dist_52w_high_pct": st.column_config.NumberColumn("52W High Dist %", format="%.2f"),
                "avg_traded_value_20": st.column_config.NumberColumn("20D Avg Traded Value", format="%.0f"),
                "volume_surge": st.column_config.NumberColumn("Vol Surge", format="%.2f"),
            }
        )

    section_header(
        "Exports",
        "Download Scanner Outputs",
        "Export liquid-screened datasets for further review."
    )

    safe_universe = (
        universe_mode.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )

    st.download_button(
        label=f"Download Qullamaggie CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(q_screen),
        file_name=f"qullamaggie_{safe_universe}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Minervini CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(m_screen),
        file_name=f"minervini_{safe_universe}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Consensus CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(c_screen),
        file_name=f"consensus_{safe_universe}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label=f"Download Metrics CSV ({universe_mode})",
        data=dataframe_to_csv_bytes(filtered_metrics),
        file_name=f"metrics_{safe_universe}.csv",
        mime="text/csv",
        use_container_width=True
    )
