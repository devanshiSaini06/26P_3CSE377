# PT377: Sentinel-2 Multispectral Change Detection for Monitoring Urban Expansion and Loss of Water Bodies (2018–2026)

**Institution:** School of Computer Science and Engineering, IILM University, Greater Noida  
**Team Members:** Shivani (2410031096), Devanshi Saini (2410031106), Saurav Raj (2410031136), Mohit Sharma (2410031144)  
**Supervisor:** Mr. Amit Agrawal (Associate Professor)

---

## 1. Software Architecture & Directory Structure

```text
PT377_Sentinel2_Urban_Water_Change_Detection/
├── app.py                                   # Main 4-View Streamlit Dashboard entrypoint
├── requirements.txt                         # Python package dependencies
├── run_pipeline.sh / run_pipeline.bat       # One-click verification & test runner scripts
├── pipeline/                                # Modular Google Earth Engine & Matrix Engine
│   ├── __init__.py
│   ├── config.py                            # ROIs, GAUL boundaries, spectral bands, constants
│   ├── cloud_masking.py                     # Sentinel-2 QA60 + SCL cloud masking & composites
│   ├── spectral_indices.py                  # NDVI, MNDWI, NDBI (GEE & 2D NumPy matrix math)
│   ├── classifier.py                        # Patched v2 2021-anchored RF + 3-yr majority filter
│   ├── matrix_engine.py                     # 2D image-to-matrix & 4x4 transition cross-tabulation
│   ├── sanity_checker.py                    # Step-2 automated sanity check verifier
│   ├── validation.py                        # Independent Google Earth confusion matrix calculator
│   └── gee_pipeline.py                      # CLI entrypoint (--stage full / --stage verify)
├── dashboard/                               # Modular 4-View Streamlit UI Components
│   ├── __init__.py
│   ├── data_loader.py                       # Loads CSVs & SQLite relational view
│   ├── view_trends.py                       # View 1: Multi-temporal LULC & monsoon water trends
│   ├── view_maps.py                         # View 2: 2D Satellite Matrix & Index Comparator
│   ├── view_matrix.py                       # View 3: 4x4 Post-Classification Change Matrix
│   └── view_accuracy.py                     # View 4: RF Accuracy, Validation & Sanity Checks
├── data/                                    # Analytical Database (CSVs + SQLite + KML)
│   ├── area_stats.csv                       # 145 lines (Patched v2 smoothed class areas)
│   ├── area_stats_raw.csv                   # 145 lines (Raw 2021-anchored RF class areas)
│   ├── accuracy.csv                         # 37 lines (2021 holdout & 2020 cross-year check)
│   ├── change_matrix.csv                    # 33 lines (2018->2026 4x4 transition matrices)
│   ├── validation_points_google_earth.csv   # 160 stratified ground-truth validation points
│   ├── validation_points.kml                # Google Earth Pro KML placemarks
│   └── pt377_geospatial.db                  # SQLite Relational Database with SQL Views
├── tests/
│   └── test_pipeline_and_dashboard.py       # 9 Passing Unit Tests (pytest & unittest compatible)
├── scripts/
│   └── local_matrix_demo.py                 # Standalone 2D NumPy matrix comparison script
├── web_prototype/                           # Standalone Browser Prototype (No Server Needed)
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── docs/                                    # Corrected Reports & [FILL] Documentation
    ├── Phase_I_Report_Corrected_PT377.md
    └── Mid_Term_and_Phase_III_Updated_Sections.md
```

---

## 2. Quick-Start Guide

### A. Run the 9 Unit Tests & Sanity Checks
```bash
python -m unittest discover -s tests -v
python pipeline/gee_pipeline.py --stage verify
```

### B. Re-Run Live Google Earth Engine Pipeline (Step 1 & Step 6)
```bash
earthengine authenticate
rm data/area_stats.csv data/area_stats_raw.csv data/accuracy.csv data/change_matrix.csv
python pipeline/gee_pipeline.py --stage full --project YOUR_PROJECT_ID --use-official-boundaries
```

### C. Launch the 4-View Streamlit Dashboard Locally (Step 8)
```bash
streamlit run app.py
```

### D. Open the Standalone Browser Prototype
Double-click `web_prototype/index.html` in any web browser.
