#!/usr/bin/env bash
set -e
echo "=== PT377: Running 9 Automated Unit Tests ==="
python3 -m unittest discover -s tests -v
echo ""
echo "=== PT377: Running Step-2 Sanity Checks on CSV Database ==="
python3 pipeline/gee_pipeline.py --stage verify
echo ""
echo "=== PT377: Running Local 2D NumPy Matrix Conversion Demo ==="
python3 scripts/local_matrix_demo.py
