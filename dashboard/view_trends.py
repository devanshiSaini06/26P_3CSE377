"""
Dashboard View 1: Multi-Temporal LULC Trends & Pre/Post-Monsoon Water Analysis (2018-2026).
"""
import streamlit as st
import pandas as pd
from dashboard.data_loader import compute_urban_water_correlation, query_sqlite_comparison


def render_trends_view(datasets, city, season, show_raw_overlay=False):
    st.subheader(f"View 1: Multi-Temporal LULC & Water Spread Trends — {city} ({season})")
    area_df = datasets["area"]
    raw_df = datasets["raw"]

    stats = compute_urban_water_correlation(area_df, city, season)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Built-up Expansion (2018→2026)",
        f"{stats['built_2026']:.2f} km²",
        f"+{stats['built_pct_change']:.2f}% (from {stats['built_2018']:.1f} km²)",
    )
    col2.metric(
        "Surface Water Spread (2018→2026)",
        f"{stats['water_2026']:.2f} km²",
        f"{stats['water_pct_change']:.2f}% (from {stats['water_2018']:.1f} km²)",
        delta_color="inverse",
    )
    col3.metric(
        "Urban vs. Water Correlation (r)",
        f"r = {stats['pearson_r']:.3f}",
        "Strong Inverse Relationship",
    )
    col4.metric(
        "Classifier Mode",
        "2021 Fixed RF + 3-Yr Maj",
        "Non-Reversion Active",
    )

    sub_sm = area_df[(area_df["city"] == city) & (area_df["season"] == season)]
    piv_sm = sub_sm.pivot(index="year", columns="class_name", values="area_km2")

    st.markdown("#### Annual Class Area Trajectories (km², 2018–2026)")
    st.line_chart(piv_sm[["Built-up", "Vegetation", "Barren", "Water"]])

    if show_raw_overlay:
        st.markdown("#### Patched Smoothed (`area_stats.csv`) vs. Raw RF (`area_stats_raw.csv`) Built-up Area")
        sub_raw = raw_df[(raw_df["city"] == city) & (raw_df["season"] == season) & (raw_df["class_name"] == "Built-up")]
        sub_b = sub_sm[sub_sm["class_name"] == "Built-up"]
        comp_df = pd.DataFrame({
            "Year": sub_b["year"].values,
            "Patched_v2_Smoothed_Built_Up_km2": sub_b["area_km2"].values,
            "Raw_2021_RF_Built_Up_km2": sub_raw["area_km2"].values,
        }).set_index("Year")
        st.line_chart(comp_df)

    st.markdown("#### Seasonal Hydrology Check: Pre-Monsoon vs. Post-Monsoon Surface Water (km²)")
    w_df = area_df[(area_df["city"] == city) & (area_df["class_name"] == "Water")]
    w_piv = w_df.pivot(index="year", columns="season", values="area_km2")
    st.bar_chart(w_piv[["Pre-Monsoon", "Post-Monsoon"]])

    with st.expander("View Underlying SQLite Relational Table (vw_urban_water_comparison)"):
        sql_df = query_sqlite_comparison(city=city, season=season)
        st.dataframe(sql_df, use_container_width=True)
