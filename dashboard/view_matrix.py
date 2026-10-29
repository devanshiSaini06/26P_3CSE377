"""
Dashboard View 3: Post-Classification 4x4 LULC Change Matrix (2018 -> 2026).
"""
import streamlit as st
import pandas as pd


def render_matrix_view(datasets, city, season):
    st.subheader(f"View 3: Post-Classification 4×4 LULC Transition Matrix (2018 → 2026) — {city}")
    chg_df = datasets["change_matrix"]
    city_chg = chg_df[chg_df["city"] == city].copy()

    col_metric = "area_post_monsoon_km2" if season == "Post-Monsoon" else "area_pre_monsoon_km2"

    piv_mat = city_chg.pivot(index="from_class", columns="to_class", values=col_metric)
    ordered_cols = ["Built-up", "Water", "Vegetation", "Barren"]
    piv_mat = piv_mat.reindex(index=ordered_cols, columns=ordered_cols)

    st.markdown(f"#### 2018 (Rows) → 2026 (Columns) Transition Matrix in km² ({season})")
    st.dataframe(piv_mat.style.format("{:.2f}"), use_container_width=True)

    # Highlight key ecological conversions into Built-up
    water_to_built = float(piv_mat.loc["Water", "Built-up"])
    veg_to_built = float(piv_mat.loc["Vegetation", "Built-up"])
    barren_to_built = float(piv_mat.loc["Barren", "Built-up"])
    built_retention = float(piv_mat.loc["Built-up", "Built-up"] / piv_mat.loc["Built-up"].sum() * 100.0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Water → Built-up Encroachment", f"{water_to_built:.2f} km²", "Direct Wetland Loss", delta_color="inverse")
    c2.metric("Vegetation → Built-up Conversion", f"{veg_to_built:.2f} km²", "Green Cover Loss", delta_color="inverse")
    c3.metric("Barren → Built-up Development", f"{barren_to_built:.2f} km²", "Peri-Urban Infill")
    c4.metric("2018 Built-up Retention", f"{built_retention:.1f}%", "Patched v2 Stability")

    st.markdown("#### Full Transition Table (`change_matrix.csv` Subset)")
    st.dataframe(city_chg, use_container_width=True)
