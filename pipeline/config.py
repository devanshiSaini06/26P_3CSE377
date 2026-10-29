"""
Configuration constants, ROI coordinates, spectral bands, and LULC class schema
for Project PT377 (Greater Noida & Bengaluru, 2018-2026).
"""

PROJECT_ID_CODE = "PT377"
STUDY_YEARS = list(range(2018, 2027))  # 2018 through 2026 inclusive
ANCHOR_TRAINING_YEAR = 2021
CROSS_CHECK_YEAR = 2020

CLASSES = {
    0: "Built-up",
    1: "Water",
    2: "Vegetation",
    3: "Barren",
}

CLASS_COLORS = {
    "Built-up": "#ef4444",
    "Water": "#0ea5e9",
    "Vegetation": "#22c55e",
    "Barren": "#eab308",
}

SEASONS = {
    "Pre-Monsoon": ("03-01", "05-31"),
    "Post-Monsoon": ("10-01", "12-15"),
}

# Bounding boxes [west, south, east, north] in WGS84 (EPSG:4326)
CITY_BOUNDING_BOXES = {
    "Greater Noida": [77.40, 28.40, 77.65, 28.60],
    "Bengaluru": [77.45, 12.83, 77.75, 13.12],
}

# FAO GAUL Level-2 Official District Names for Step 6 (--use-official-boundaries)
OFFICIAL_GAUL_DISTRICTS = {
    "Greater Noida": ("Uttar Pradesh", "Gautam Buddha Nagar"),
    "Bengaluru": ("Karnataka", "Bangalore Urban"),
}

SENTINEL2_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"
WORLDCOVER_COLLECTION = "ESA/WorldCover/v200"

REFLECTANCE_BANDS = ["B2", "B3", "B4", "B8", "B11", "B12"]
INDEX_BANDS = ["NDVI", "MNDWI", "NDBI"]
FEATURE_BANDS = REFLECTANCE_BANDS + INDEX_BANDS
