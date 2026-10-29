"""
Automated Sanity-Check Module (Step 2 of Project Checklist).
Verifies:
  1. Line counts of exported CSVs (145, 145, 37, 33).
  2. Built-up area rises or holds steady between 2018 and 2026 in both cities.
  3. Post-Monsoon surface water area exceeds Pre-Monsoon surface water area.
  4. Change matrix shows plausible built-up retention (>90%) rather than the v1 62.5% churn.
"""
import os
import pandas as pd


def run_all_sanity_checks(data_dir="data"):
    area_path = os.path.join(data_dir, "area_stats.csv")
    raw_path = os.path.join(data_dir, "area_stats_raw.csv")
    acc_path = os.path.join(data_dir, "accuracy.csv")
    chg_path = os.path.join(data_dir, "change_matrix.csv")

    df_area = pd.read_csv(area_path)
    df_raw = pd.read_csv(raw_path)
    df_acc = pd.read_csv(acc_path)
    df_chg = pd.read_csv(chg_path)

    results = []

    # Check 1: File line counts (header + rows = 145, 145, 37, 33)
    line_counts = {
        "area_stats.csv": len(df_area) + 1,
        "area_stats_raw.csv": len(df_raw) + 1,
        "accuracy.csv": len(df_acc) + 1,
        "change_matrix.csv": len(df_chg) + 1,
    }
    c1_pass = (
        line_counts["area_stats.csv"] == 145
        and line_counts["area_stats_raw.csv"] == 145
        and line_counts["accuracy.csv"] == 37
        and line_counts["change_matrix.csv"] == 33
    )
    results.append({
        "check": "CSV Schema & Row Counts (145, 145, 37, 33 lines)",
        "passed": bool(c1_pass),
        "details": str(line_counts),
    })

    # Check 2: Built-up monotonic growth (2018 -> 2026)
    c2_pass = True
    c2_details = []
    for city in ["Greater Noida", "Bengaluru"]:
        sub = df_area[
            (df_area["city"] == city)
            & (df_area["season"] == "Post-Monsoon")
            & (df_area["class_name"] == "Built-up")
        ].sort_values("year")
        vals = sub["area_km2"].values
        is_monotonic = bool((vals[-1] > vals[0]) and all(vals[i] <= vals[i + 1] + 0.01 for i in range(len(vals) - 1)))
        c2_pass = c2_pass and is_monotonic
        pct_gain = ((vals[-1] - vals[0]) / vals[0]) * 100.0
        c2_details.append(f"{city}: {vals[0]:.1f} -> {vals[-1]:.1f} km2 (+{pct_gain:.1f}%)")
    results.append({
        "check": "Built-up Area Rises / Holds Steady (2018-2026)",
        "passed": bool(c2_pass),
        "details": " | ".join(c2_details),
    })

    # Check 3: Post-Monsoon Water > Pre-Monsoon Water
    c3_pass = True
    c3_details = []
    for city in ["Greater Noida", "Bengaluru"]:
        w_pre = df_area[
            (df_area["city"] == city)
            & (df_area["season"] == "Pre-Monsoon")
            & (df_area["class_name"] == "Water")
        ]["area_km2"].mean()
        w_post = df_area[
            (df_area["city"] == city)
            & (df_area["season"] == "Post-Monsoon")
            & (df_area["class_name"] == "Water")
        ]["area_km2"].mean()
        c3_pass = c3_pass and bool(w_post > w_pre)
        c3_details.append(f"{city}: Post={w_post:.2f} km2 > Pre={w_pre:.2f} km2")
    results.append({
        "check": "Post-Monsoon Surface Water Exceeds Pre-Monsoon Water",
        "passed": bool(c3_pass),
        "details": " | ".join(c3_details),
    })

    # Check 4: Change Matrix Plausibility (Built-up retention >= 95%)
    c4_pass = True
    c4_details = []
    for city in ["Greater Noida", "Bengaluru"]:
        built_rows = df_chg[(df_chg["city"] == city) & (df_chg["from_class"] == "Built-up")]
        total_2018_built = built_rows["area_km2"].sum()
        retained_built = built_rows[built_rows["to_class"] == "Built-up"]["area_km2"].sum()
        retention_pct = (retained_built / total_2018_built) * 100.0 if total_2018_built > 0 else 0.0
        c4_pass = c4_pass and bool(retention_pct >= 95.0)
        c4_details.append(f"{city} Built-up Retention: {retention_pct:.1f}%")
    results.append({
        "check": "Change Matrix Plausibility (No Unphysical Built-up Reversion)",
        "passed": bool(c4_pass),
        "details": " | ".join(c4_details),
    })

    return results
