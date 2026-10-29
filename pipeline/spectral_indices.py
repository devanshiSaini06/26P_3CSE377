"""
Spectral Index Computation Module (NDVI, MNDWI, NDBI).
Supports both Google Earth Engine server-side ee.Image objects and local 2D NumPy matrices.
"""
import numpy as np


def add_spectral_indices_gee(image):
    """
    Adds Normalized Difference Vegetation Index (NDVI),
    Modified Normalized Difference Water Index (MNDWI), and
    Normalized Difference Built-up Index (NDBI) bands to an ee.Image.
    """
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    mndwi = image.normalizedDifference(["B3", "B11"]).rename("MNDWI")
    ndbi = image.normalizedDifference(["B11", "B8"]).rename("NDBI")
    return image.addBands([ndvi, mndwi, ndbi])


def compute_indices_numpy(b3_green, b4_red, b8_nir, b11_swir1, eps=1e-8):
    """
    Converts 2D Sentinel-2 spectral band arrays into 2D spectral index matrices:
      - NDVI  = (B8 - B4)  / (B8 + B4)   [Vegetation]
      - MNDWI = (B3 - B11) / (B3 + B11)  [Surface Water]
      - NDBI  = (B11 - B8) / (B11 + B8)  [Built-up Impervious Surfaces]
    Returns a dictionary of 2D float matrices clipped to [-1.0, 1.0].
    """
    b3 = np.asarray(b3_green, dtype=np.float64)
    b4 = np.asarray(b4_red, dtype=np.float64)
    b8 = np.asarray(b8_nir, dtype=np.float64)
    b11 = np.asarray(b11_swir1, dtype=np.float64)

    ndvi = np.clip((b8 - b4) / (b8 + b4 + eps), -1.0, 1.0)
    mndwi = np.clip((b3 - b11) / (b3 + b11 + eps), -1.0, 1.0)
    ndbi = np.clip((b11 - b8) / (b11 + b8 + eps), -1.0, 1.0)

    return {
        "NDVI": ndvi,
        "MNDWI": mndwi,
        "NDBI": ndbi,
    }
