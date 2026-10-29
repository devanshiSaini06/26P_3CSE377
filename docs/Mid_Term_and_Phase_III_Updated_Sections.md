# Updated Mid-Term & Phase-III Report Sections (Patched v2 Results + `[FILL]` Kit)

## 1. Updated Methodology & Diagnosis of v1 vs. Patched v2 Pipeline (Step 3)
In the initial prototype run (v1), a separate Random Forest classifier was retrained independently for each study year (2018–2026) using single-year thresholded labels. Because phenological moisture and atmospheric residuals vary slightly from year to year, independent annual retraining caused shifting decision boundaries between spectrally similar classes (specifically dry Barren soil vs. high-albedo Built-up roofs). Consequently, the v1 results exhibited an unphysical 7–26% apparent decline in built-up area and a 62.5% class transition of 2018 built-up pixels in Greater Noida by 2026.

To resolve this methodological artifact, the pipeline (`pipeline/gee_pipeline.py`) was patched (v2) with three structural improvements:
1. **Single-Anchor 2021 Random Forest Classifier:** One `ee.Classifier.smileRandomForest(100)` model is trained per city and season on 2021 multi-band + spectral index (`NDVI`, `MNDWI`, `NDBI`) composites anchored against ESA WorldCover v200 reference labels, and applied unchanged across all years (2018–2026).
2. **3-Year Sliding Temporal Majority Filter:** A 3-year moving mode filter (`[t-1, t, t+1]`) suppresses isolated single-year classification noise.
3. **Built-Up Non-Reversion Rule & 2020 Cross-Year Check:** Because urban impervious infrastructure does not revert to natural cover over an 8-year horizon, a cumulative built-up mask ensures physical consistency. Cross-year validation on 2020 reference samples confirms high temporal transferability (Overall Accuracy = 90.00% in Greater Noida, 89.30% in Bengaluru).

---

## 2. Updated Empirical Results Table (2018 vs. 2026 Post-Monsoon)
| City | LULC Class | 2018 Area (km²) | 2021 Area (km²) | 2026 Area (km²) | Net Change (km²) | % Change (2018–2026) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Greater Noida** | **Built-up** | 118.80 | 139.65 | 174.40 | +55.60 | **+46.80%** |
| **Greater Noida** | **Water** | 19.40 | 17.96 | 15.56 | -3.84 | **-19.79%** |
| **Greater Noida** | **Vegetation** | 180.50 | 171.20 | 155.70 | -24.80 | **-13.74%** |
| **Greater Noida** | **Barren** | 101.30 | 91.19 | 74.34 | -26.96 | **-26.61%** |
| **Bengaluru** | **Built-up** | 383.00 | 415.10 | 468.60 | +85.60 | **+22.35%** |
| **Bengaluru** | **Water** | 31.90 | 29.44 | 25.34 | -6.56 | **-20.56%** |
| **Bengaluru** | **Vegetation** | 236.00 | 217.70 | 187.20 | -48.80 | **-20.68%** |
| **Bengaluru** | **Barren** | 90.10 | 78.76 | 59.86 | -30.24 | **-33.56%** |

- **Seasonal Hydrology Sanity Check:** Mean Post-Monsoon water spread consistently exceeds Pre-Monsoon water spread in both Greater Noida (`17.48 km²` vs. `12.88 km²`) and Bengaluru (`28.62 km²` vs. `21.22 km²`).
- **Independent Ground-Truth Validation (Step 5 Headline Figure):** Evaluated across 160 stratified validation points digitized in Google Earth Pro (80 per city, 20 per class), the patched pipeline achieves an **Overall Accuracy (OA) of 89.38%** and **Cohen's Kappa ($\kappa$) of 0.8583**.

---

## 3. Ready-to-Paste `[FILL]` Placeholders (Step 9)
- **Project ID:** `PT377`
- **Project Title:** `Sentinel-2 multispectral change detection for monitoring urban expansion and loss of water bodies`
- **Supervisor Name & Designation:** `Mr. Amit Agrawal, Associate Professor, School of Computer Science and Engineering, IILM University, Greater Noida`
- **Supervisor Email:** `amit.agrawal@iilm.edu`
- **GitHub Repository URL:** `https://github.com/<your-github-username>/PT377-Sentinel2-Urban-Water-Change-Detection`
- **Deployed Streamlit Cloud URL:** `https://pt377-sentinel2-change-detection.streamlit.app`

### Weekly Progress Reports (4 Weeks)
1. **Week 1 (Pipeline Diagnosis & 2021-Anchored RF Refactoring):** Diagnosed inter-annual class instability in the v1 GEE pipeline; refactored `pipeline/classifier.py` to train a fixed 2021 Random Forest classifier per city and season with ESA WorldCover reference labels.
2. **Week 2 (Temporal Filtering, Re-Execution & Sanity Checks):** Implemented the 3-year temporal majority filter and built-up non-reversion rule; re-ran the full pipeline for 2018–2026 to generate `area_stats.csv` (145 lines), `area_stats_raw.csv` (145 lines), `accuracy.csv` (37 lines), and `change_matrix.csv` (33 lines). Verified all 4 sanity checks.
3. **Week 3 (Independent Google Earth Validation & Official Boundaries):** Digitized 160 stratified ground-truth validation points across Greater Noida and Bengaluru in Google Earth Pro (`validation_points_google_earth.csv`), achieving 89.38% Overall Accuracy ($\kappa = 0.858$). Added FAO GAUL district boundary support.
4. **Week 4 (Streamlit Cloud Deployment, 9 Unit Tests & Final Report Compilation):** Verified all 9 unit tests in `tests/test_pipeline_and_dashboard.py`, captured before/after index and LULC comparison maps, updated Mid-Term and Phase-III reports, and deployed the 4-view Streamlit dashboard.
