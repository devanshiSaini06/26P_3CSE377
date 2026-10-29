"""
Automated Test Suite for Project PT377 (9 Passing Tests).
Compatible with both `pytest` and standard `python -m unittest`:
  pytest tests/
  python -m unittest discover -s tests
"""
import os
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.spectral_indices import compute_indices_numpy
from pipeline.classifier import apply_temporal_filter_and_non_reversion_numpy
from pipeline.matrix_engine import compute_transition_matrix_numpy
from pipeline.sanity_checker import run_all_sanity_checks
from pipeline.validation import evaluate_independent_validation

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


class TestPT377PipelineAndDashboard(unittest.TestCase):
    def test_1_area_stats_row_count_and_schema(self):
        """Test 1: Verifies area_stats.csv has 144 data rows (145 lines) and required columns."""
        df = pd.read_csv(os.path.join(DATA_DIR, "area_stats.csv"))
        self.assertEqual(len(df), 144)
        for col in ["city", "season", "year", "class_id", "class_name", "area_km2"]:
            self.assertIn(col, df.columns)

    def test_2_area_stats_raw_consistency(self):
        """Test 2: Verifies area_stats_raw.csv has 144 data rows and consistent total city areas."""
        df_raw = pd.read_csv(os.path.join(DATA_DIR, "area_stats_raw.csv"))
        self.assertEqual(len(df_raw), 144)
        gn_totals = df_raw[df_raw["city"] == "Greater Noida"].groupby(["season", "year"])["area_km2"].sum()
        self.assertTrue(np.allclose(gn_totals.values, 420.0, atol=0.5))

    def test_3_accuracy_csv_bounds_and_2020_check(self):
        """Test 3: Verifies accuracy.csv has 36 data rows (37 lines) and includes 2020 cross-year check."""
        df_acc = pd.read_csv(os.path.join(DATA_DIR, "accuracy.csv"))
        self.assertEqual(len(df_acc), 36)
        self.assertTrue((df_acc["overall_accuracy"] >= 0.80).all() and (df_acc["overall_accuracy"] <= 1.0).all())
        self.assertIn("2020_CrossYear_Check", df_acc["eval_type"].values)

    def test_4_change_matrix_row_count_and_conservation(self):
        """Test 4: Verifies change_matrix.csv has 32 data rows (33 lines) and conserves city area."""
        df_chg = pd.read_csv(os.path.join(DATA_DIR, "change_matrix.csv"))
        self.assertEqual(len(df_chg), 32)
        gn_sum = df_chg[df_chg["city"] == "Greater Noida"]["area_km2"].sum()
        blr_sum = df_chg[df_chg["city"] == "Bengaluru"]["area_km2"].sum()
        self.assertLess(abs(gn_sum - 420.0), 1.0)
        self.assertLess(abs(blr_sum - 741.0), 1.0)

    def test_5_built_up_monotonic_growth_sanity(self):
        """Test 5: Verifies Patched v2 built-up area rises monotonically from 2018 to 2026."""
        checks = run_all_sanity_checks(DATA_DIR)
        built_check = [c for c in checks if "Built-up Area Rises" in c["check"]][0]
        self.assertTrue(built_check["passed"])

    def test_6_post_monsoon_water_exceeds_pre_monsoon(self):
        """Test 6: Verifies Post-Monsoon surface water area exceeds Pre-Monsoon water area."""
        checks = run_all_sanity_checks(DATA_DIR)
        water_check = [c for c in checks if "Post-Monsoon Surface Water" in c["check"]][0]
        self.assertTrue(water_check["passed"])

    def test_7_spectral_indices_matrix_math(self):
        """Test 7: Verifies 2D NumPy matrix calculation of NDVI, MNDWI, and NDBI."""
        b3 = np.array([[0.15, 0.06]], dtype=float)
        b4 = np.array([[0.05, 0.20]], dtype=float)
        b8 = np.array([[0.03, 0.15]], dtype=float)
        b11 = np.array([[0.02, 0.28]], dtype=float)
        indices = compute_indices_numpy(b3, b4, b8, b11)
        self.assertGreater(indices["MNDWI"][0, 0], 0.5)
        self.assertGreater(indices["NDBI"][0, 1], 0.2)

    def test_8_temporal_majority_and_non_reversion_filter(self):
        """Test 8: Verifies 3-year majority filter and built-up non-reversion rule on 2D matrices."""
        m0 = np.array([[0, 2], [1, 3]])
        m1 = np.array([[3, 2], [1, 3]])
        m2 = np.array([[0, 0], [1, 3]])
        smoothed = apply_temporal_filter_and_non_reversion_numpy([m0, m1, m2])
        self.assertEqual(smoothed[0][0, 0], 0)
        self.assertEqual(smoothed[1][0, 0], 0)
        self.assertEqual(smoothed[2][0, 0], 0)

    def test_9_transition_matrix_computation_and_validation(self):
        """Test 9: Verifies 4x4 transition matrix computation and independent Google Earth validation."""
        m18 = np.array([[1, 1], [2, 0]])
        m26 = np.array([[0, 1], [0, 0]])
        df_mat = compute_transition_matrix_numpy(m18, m26, pixel_area_km2=1.0)
        w_to_b = df_mat[(df_mat["from_class_id"] == 1) & (df_mat["to_class_id"] == 0)]["area_km2"].values[0]
        self.assertEqual(w_to_b, 1.0)

        val_res = evaluate_independent_validation(os.path.join(DATA_DIR, "validation_points_google_earth.csv"))
        self.assertEqual(val_res["n_points"], 160)
        self.assertGreater(val_res["overall_accuracy"], 0.85)


if __name__ == "__main__":
    unittest.main(verbosity=2)
