"""
Main Streamlit Cloud Application Entrypoint for Project PT377.
Run locally via:
  streamlit run app.py
"""
import streamlit as st
from dashboard.data_loader import load_all_datasets
from dashboard.view_trends import render_trends_view
from dashboard.view_maps import render_maps_view
from dashboard.view_matrix import render_matrix_view
from dashboard.view_accuracy import render_accuracy_view

st.set_page_config(
    page_title="PT377 | Sentinel-2 Urban & Water Body Change Detection (2018-2026)",
    page_icon="🛰️",
    layout="wide",
)

st.title("🛰️ Sentinel-2 Multispectral Change Detection Dashboard (2018–2026)")
st.caption(
    "**Major Project PT377** | School of Computer Science & Engineering, IILM University, Greater Noida | "
    "Team: Shivani (2410031096), Devanshi Saini (2410031106), Saurav Raj (2410031136), Mohit Sharma (2410031144) | "
    "Supervisor: Mr. Amit Agrawal"
)

datasets = load_all_datasets("data")

with st.sidebar:
    st.header("⚙️ Study Controls")
    selected_city = st.selectbox("Select Study Area (City):", ["Greater Noida", "Bengaluru"])
    selected_season = st.radio("Select Hydrological Season:", ["Post-Monsoon", "Pre-Monsoon"])
    show_raw = st.checkbox("Compare with Raw Unsmoothed RF (area_stats_raw.csv)", value=True)
    st.markdown("---")
    st.markdown(
        "**Pipeline Architecture:**\n"
        "- **Sensor:** Sentinel-2 MSI Level-2A (10m)\n"
        "- **Database:** GEE `COPERNICUS/S2_SR_HARMONIZED` + SQLite/CSV\n"
        "- **Classifier:** 2021-Anchored RF (100 trees) + 3-Yr Majority Filter + Non-Reversion Rule"
    )

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Area & Water Trends",
    "🗺️ 2. Spatial Matrix & Indices",
    "🔄 3. 4×4 Change Matrix",
    "✅ 4. Accuracy & Sanity Checks",
])

with tab1:
    render_trends_view(datasets, selected_city, selected_season, show_raw_overlay=show_raw)

with tab2:
    render_maps_view(datasets, selected_city, selected_season)

with tab3:
    render_matrix_view(datasets, selected_city, selected_season)

with tab4:
    render_accuracy_view(datasets, selected_city, selected_season)
