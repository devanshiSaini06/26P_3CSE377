"""
Standalone Script: Converts Sentinel-2 Multispectral Bands (B3, B4, B8, B11)
into 2D Spectral Index Matrices (NDVI, MNDWI, NDBI), classifies Built-up, Water,
Vegetation, and Barren pixels, applies the 3-year majority filter + non-reversion rule,
and prints the 4x4 Transition Matrix (2018 -> 2026).

Run via:
  python scripts/local_matrix_demo.py
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.spectral_indices import compute_indices_numpy
from pipeline.classifier import apply_temporal_filter_and_non_reversion_numpy
from pipeline.matrix_engine import compute_transition_matrix_numpy
from dashboard.view_maps import generate_hotspot_bands


def main():
    for city in ["Greater Noida", "Bengaluru"]:
        print("=" * 72)
        print(f"STUDY AREA: {city} | 2D Matrix Conversion & LULC Comparison (2018-2026)")
        print("=" * 72)

        yearly_raw_matrices = []
        for yr in range(2018, 2027):
            b3, b4, b8, b11, lulc = generate_hotspot_bands(city, yr, grid_size=50)
            indices = compute_indices_numpy(b3, b4, b8, b11)
            yearly_raw_matrices.append(lulc)
            if yr in (2018, 2021, 2026):
                print(
                    f"  Year {yr} | Matrix Shape: {lulc.shape} | "
                    f"Mean NDVI={indices['NDVI'].mean():.3f}, "
                    f"Mean MNDWI={indices['MNDWI'].mean():.3f}, "
                    f"Mean NDBI={indices['NDBI'].mean():.3f}"
                )

        smoothed_matrices = apply_temporal_filter_and_non_reversion_numpy(yearly_raw_matrices)
        df_trans = compute_transition_matrix_numpy(
            smoothed_matrices[0], smoothed_matrices[-1], pixel_area_km2=0.01
        )
        piv = df_trans.pivot(index="from_class", columns="to_class", values="area_km2")
        print("\nPost-Classification 4x4 Transition Matrix (2018 Rows -> 2026 Columns, km²):")
        print(piv.round(3))
        print()


if __name__ == "__main__":
    main()
