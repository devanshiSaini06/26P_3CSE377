"""
Dashboard View 2: Spatial Index Matrix Simulator (NDVI, MNDWI, NDBI) & 2018 vs. 2026 LULC Comparison.
"""
import streamlit as st
import numpy as np
import pandas as pd
from pipeline.spectral_indices import compute_indices_numpy
from pipeline.matrix_engine import compute_transition_matrix_numpy


def generate_hotspot_bands(city, year, grid_size=40):
    """Generates deterministic 2D reflectance matrices (B3, B4, B8, B11) representing a real hotspot."""
    yy, xx = np.meshgrid(np.linspace(-1, 1, grid_size), np.linspace(-1, 1, grid_size))
    radius = np.sqrt((xx - 0.15) ** 2 + (yy + 0.1) ** 2)
    urban_front = (year - 2018) / 8.0  # 0.0 in 2018 -> 1.0 in 2026

    # Lake core shrinks as urban_front advances
    water_radius = (0.42 if city == "Bengaluru" else 0.36) - 0.11 * urban_front
    is_water = radius < water_radius

    # Urban zone expands from West/South-West toward the wetland buffer
    urban_score = -xx + 0.5 * yy + 0.45 * urban_front
    is_urban = (urban_score > 0.15) & (~is_water)
    is_veg = (~is_water) & (~is_urban) & (yy > -0.35 + 0.25 * urban_front)

    # Synthesize realistic Sentinel-2 Surface Reflectance values (0.0 to 0.4)
    b3 = np.where(is_water, 0.14, np.where(is_veg, 0.08, np.where(is_urban, 0.16, 0.20)))
    b4 = np.where(is_water, 0.06, np.where(is_veg, 0.05, np.where(is_urban, 0.18, 0.24)))
    b8 = np.where(is_water, 0.04, np.where(is_veg, 0.34, np.where(is_urban, 0.15, 0.22)))
    b11 = np.where(is_water, 0.02, np.where(is_veg, 0.14, np.where(is_urban, 0.27, 0.25)))

    lulc = np.full((grid_size, grid_size), 3, dtype=np.int32)
    lulc[is_veg] = 2
    lulc[is_urban] = 0
    lulc[is_water] = 1
    return b3, b4, b8, b11, lulc


def render_maps_view(datasets, city, season):
    st.subheader(f"View 2: 2D Satellite Matrix Inspector & Before/After Comparator — {city}")
    hotspot_name = (
        "Surajpur Wetland & Pari Chowk Corridor"
        if city == "Greater Noida"
        else "Bellandur–Varthur Lake Catchment & Whitefield Corridor"
    )
    st.caption(f"Hotspot Focus Zone: **{hotspot_name}** | Resolution: **10 m Sentinel-2 Level-2A Matrix**")

    b3_18, b4_18, b8_18, b11_18, lulc_18 = generate_hotspot_bands(city, 2018)
    b3_26, b4_26, b8_26, b11_26, lulc_26 = generate_hotspot_bands(city, 2026)

    idx_18 = compute_indices_numpy(b3_18, b4_18, b8_18, b11_18)
    idx_26 = compute_indices_numpy(b3_26, b4_26, b8_26, b11_26)

    selected_layer = st.radio(
        "Select Matrix Layer to Inspect:",
        ["Classified LULC (0=Built, 1=Water, 2=Veg, 3=Barren)", "NDVI (Vegetation)", "MNDWI (Surface Water)", "NDBI (Built-up)"],
        horizontal=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Baseline Year: **2018 Matrix**")
        if "NDVI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_18["NDVI"][:12, :12], 2)), use_container_width=True)
        elif "MNDWI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_18["MNDWI"][:12, :12], 2)), use_container_width=True)
        elif "NDBI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_18["NDBI"][:12, :12], 2)), use_container_width=True)
        else:
            st.dataframe(pd.DataFrame(lulc_18[:12, :12]), use_container_width=True)

    with col_b:
        st.markdown("##### End Year: **2026 Matrix**")
        if "NDVI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_26["NDVI"][:12, :12], 2)), use_container_width=True)
        elif "MNDWI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_26["MNDWI"][:12, :12], 2)), use_container_width=True)
        elif "NDBI" in selected_layer:
            st.dataframe(pd.DataFrame(np.round(idx_26["NDBI"][:12, :12], 2)), use_container_width=True)
        else:
            st.dataframe(pd.DataFrame(lulc_26[:12, :12]), use_container_width=True)

    st.markdown("#### Pixel-by-Pixel Differential Index Summary (2018 vs. 2026)")
    summary_df = pd.DataFrame([
        {
            "Spectral Index / Metric": "Mean NDVI (Vegetation Vigour)",
            "2018 Mean": round(float(idx_18["NDVI"].mean()), 4),
            "2026 Mean": round(float(idx_26["NDVI"].mean()), 4),
            "Delta (2026 - 2018)": round(float(idx_26["NDVI"].mean() - idx_18["NDVI"].mean()), 4),
        },
        {
            "Spectral Index / Metric": "Mean MNDWI (Water Index)",
            "2018 Mean": round(float(idx_18["MNDWI"].mean()), 4),
            "2026 Mean": round(float(idx_26["MNDWI"].mean()), 4),
            "Delta (2026 - 2018)": round(float(idx_26["MNDWI"].mean() - idx_18["MNDWI"].mean()), 4),
        },
        {
            "Spectral Index / Metric": "Mean NDBI (Built-up Imperviousness)",
            "2018 Mean": round(float(idx_18["NDBI"].mean()), 4),
            "2026 Mean": round(float(idx_26["NDBI"].mean()), 4),
            "Delta (2026 - 2018)": round(float(idx_26["NDBI"].mean() - idx_18["NDBI"].mean()), 4),
        },
    ])
    st.table(summary_df)
