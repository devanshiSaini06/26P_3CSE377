"""
Data Loader & SQL/CSV Query Engine for the PT377 Streamlit Dashboard.
"""
import os
import sqlite3
import numpy as np
import pandas as pd


def load_all_datasets(data_dir="data"):
    area_df = pd.read_csv(os.path.join(data_dir, "area_stats.csv"))
    raw_df = pd.read_csv(os.path.join(data_dir, "area_stats_raw.csv"))
    acc_df = pd.read_csv(os.path.join(data_dir, "accuracy.csv"))
    chg_df = pd.read_csv(os.path.join(data_dir, "change_matrix.csv"))
    val_df = pd.read_csv(os.path.join(data_dir, "validation_points_google_earth.csv"))
    return {
        "area": area_df,
        "raw": raw_df,
        "accuracy": acc_df,
        "change_matrix": chg_df,
        "validation": val_df,
    }


def query_sqlite_comparison(db_path="data/pt377_geospatial.db", city="Greater Noida", season="Post-Monsoon"):
    """Queries the SQLite view vw_urban_water_comparison for SQL-backed comparison."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT city, season, year, built_up_km2, water_km2, vegetation_km2, barren_km2
    FROM vw_urban_water_comparison
    WHERE city = ? AND season = ?
    ORDER BY year ASC
    """
    df = pd.read_sql_query(query, conn, params=(city, season))
    conn.close()
    return df


def compute_urban_water_correlation(area_df, city, season="Post-Monsoon"):
    sub = area_df[(area_df["city"] == city) & (area_df["season"] == season)]
    piv = sub.pivot(index="year", columns="class_name", values="area_km2")
    r_val = float(np.corrcoef(piv["Built-up"], piv["Water"])[0, 1])
    built_2018 = float(piv.loc[2018, "Built-up"])
    built_2026 = float(piv.loc[2026, "Built-up"])
    water_2018 = float(piv.loc[2018, "Water"])
    water_2026 = float(piv.loc[2026, "Water"])
    return {
        "pearson_r": round(r_val, 4),
        "built_2018": built_2018,
        "built_2026": built_2026,
        "built_pct_change": round(((built_2026 - built_2018) / built_2018) * 100.0, 2),
        "water_2018": water_2018,
        "water_2026": water_2026,
        "water_pct_change": round(((water_2026 - water_2018) / water_2018) * 100.0, 2),
    }
