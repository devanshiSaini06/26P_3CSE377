"""
Independent Ground-Truth Validation Calculator (Steps 4 & 5).
Computes Overall Accuracy (OA), Cohen's Kappa, Producer's Accuracy (PA),
and User's Accuracy (UA) from independent Google Earth validation points.
"""
import numpy as np
import pandas as pd
from pipeline.config import CLASSES


def evaluate_independent_validation(csv_path="data/validation_points_google_earth.csv", city_filter=None):
    df = pd.read_csv(csv_path)
    if city_filter and city_filter != "All":
        df = df[df["city"] == city_filter]

    conf_mat = np.zeros((4, 4), dtype=int)
    for _, row in df.iterrows():
        gt = int(row["ground_truth_id"])
        pred = int(row["rf_predicted_id"])
        conf_mat[gt, pred] += 1

    total = conf_mat.sum()
    diag = np.trace(conf_mat)
    oa = diag / total if total > 0 else 0.0

    row_sums = conf_mat.sum(axis=1)
    col_sums = conf_mat.sum(axis=0)
    expected = np.sum(row_sums * col_sums) / (total * total) if total > 0 else 0.0
    kappa = (oa - expected) / (1.0 - expected) if (1.0 - expected) > 0 else 0.0

    per_class = []
    for cid, cname in CLASSES.items():
        pa = conf_mat[cid, cid] / row_sums[cid] if row_sums[cid] > 0 else 0.0
        ua = conf_mat[cid, cid] / col_sums[cid] if col_sums[cid] > 0 else 0.0
        per_class.append({
            "class_id": cid,
            "class_name": cname,
            "ground_truth_total": int(row_sums[cid]),
            "predicted_total": int(col_sums[cid]),
            "correct": int(conf_mat[cid, cid]),
            "producers_accuracy": round(float(pa), 4),
            "users_accuracy": round(float(ua), 4),
        })

    return {
        "n_points": int(total),
        "overall_accuracy": round(float(oa), 4),
        "kappa": round(float(kappa), 4),
        "confusion_matrix": conf_mat,
        "per_class_metrics": pd.DataFrame(per_class),
    }
