"""
Matrix Conversion Engine:
Converts 2D classified satellite matrices (2018 vs 2026) into class area tables
and 4x4 LULC post-classification change matrices (T = M_2018 * 10 + M_2026).
"""
import numpy as np
import pandas as pd
from pipeline.config import CLASSES


def compute_transition_matrix_numpy(matrix_2018, matrix_2026, pixel_area_km2=0.0001):
    """
    Computes the 4x4 post-classification transition matrix in km^2 between two 2D
    classified LULC matrices (values in {0, 1, 2, 3}).
    Each 10m x 10m Sentinel-2 pixel represents 100 m^2 = 0.0001 km^2.
    """
    m18 = np.asarray(matrix_2018, dtype=np.int32).ravel()
    m26 = np.asarray(matrix_2026, dtype=np.int32).ravel()
    if m18.shape != m26.shape:
        raise ValueError("2018 and 2026 LULC matrices must have identical dimensions.")

    transition_codes = m18 * 10 + m26
    rows = []
    for c_from in range(4):
        from_mask = (m18 == c_from)
        from_total_km2 = float(np.sum(from_mask) * pixel_area_km2)
        for c_to in range(4):
            code = c_from * 10 + c_to
            count = int(np.sum(transition_codes == code))
            area_km2 = round(count * pixel_area_km2, 4)
            pct = round((area_km2 / from_total_km2) * 100.0, 2) if from_total_km2 > 0 else 0.0
            rows.append({
                "from_class_id": c_from,
                "from_class": CLASSES[c_from],
                "to_class_id": c_to,
                "to_class": CLASSES[c_to],
                "transition_code": code,
                "pixel_count": count,
                "area_km2": area_km2,
                "pct_of_2018_class": pct,
            })
    return pd.DataFrame(rows)


def compute_class_areas_gee(classified_img, roi, scale=30):
    """
    Computes total area (km^2) per class (0..3) in Google Earth Engine.
    Uses scale=30 and tileScale=4 to prevent GEE memory/timeout stalls on full districts.
    """
    import ee

    area_img = ee.Image.pixelArea().divide(1e6).addBands(classified_img.rename("class"))
    stats = (
        area_img.reduceRegion(
            reducer=ee.Reducer.sum().group(groupField=1, groupName="class"),
            geometry=roi,
            scale=scale,
            tileScale=4,
            bestEffort=True,
            maxPixels=1e10,
        )
        .get("groups")
        .getInfo()
    )
    areas = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    for item in stats:
        c = int(item["class"])
        if c in areas:
            areas[c] = round(float(item["sum"]), 2)
    return areas


def compute_transition_matrix_gee(map_2018, map_2026, roi, scale=30):
    """
    Computes 4x4 transition matrix in km^2 server-side in Google Earth Engine.
    Uses scale=30 and tileScale=4 for fast execution without GEE timeout.
    """
    import ee

    transition_img = map_2018.multiply(10).add(map_2026).rename("transition")
    area_img = ee.Image.pixelArea().divide(1e6).addBands(transition_img)
    stats = (
        area_img.reduceRegion(
            reducer=ee.Reducer.sum().group(groupField=1, groupName="transition"),
            geometry=roi,
            scale=scale,
            tileScale=4,
            bestEffort=True,
            maxPixels=1e10,
        )
        .get("groups")
        .getInfo()
    )
    mat = {(i, j): 0.0 for i in range(4) for j in range(4)}
    for item in stats:
        code = int(item["transition"])
        c_from, c_to = code // 10, code % 10
        if (c_from, c_to) in mat:
            mat[(c_from, c_to)] = round(float(item["sum"]), 2)
    return mat
