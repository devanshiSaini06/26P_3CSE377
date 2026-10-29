"""
Sentinel-2 Level-2A Cloud & Shadow Masking and Seasonal Composite Builder.
Uses both QA60 bitmask (opaque & cirrus clouds) and SCL (Scene Classification Layer).
"""
from pipeline.config import SENTINEL2_COLLECTION, SEASONS, REFLECTANCE_BANDS


def mask_s2_clouds_gee(image):
    """
    Applies cloud and shadow mask to a Google Earth Engine Sentinel-2 Level-2A image
    and scales reflectance bands by 1/10000.
    """
    import ee

    qa = image.select("QA60")
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    qa_mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )

    # SCL classes to mask out: 3 (Cloud Shadow), 8 (Cloud Medium Prob), 9 (Cloud High Prob), 10 (Cirrus)
    scl = image.select("SCL")
    scl_mask = (
        scl.neq(3)
        .And(scl.neq(8))
        .And(scl.neq(9))
        .And(scl.neq(10))
    )

    combined_mask = qa_mask.And(scl_mask)
    return (
        image.updateMask(combined_mask)
        .select(REFLECTANCE_BANDS)
        .divide(10000.0)
        .copyProperties(image, ["system:time_start"])
    )


def build_seasonal_composite_gee(roi, year, season_name, max_cloud_pct=30, add_indices_fn=None):
    """
    Fetches Sentinel-2 SR scenes from Google Earth Engine for a given city ROI,
    year, and season, applies cloud masking, computes spectral indices, and returns
    the pixel-wise median composite clipped to the ROI.
    """
    import ee

    start_mmdd, end_mmdd = SEASONS[season_name]
    start_date = f"{year}-{start_mmdd}"
    end_date = f"{year}-{end_mmdd}"

    collection = (
        ee.ImageCollection(SENTINEL2_COLLECTION)
        .filterBounds(roi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_cloud_pct))
        .map(mask_s2_clouds_gee)
    )

    if add_indices_fn is not None:
        collection = collection.map(add_indices_fn)

    return collection.median().clip(roi)
