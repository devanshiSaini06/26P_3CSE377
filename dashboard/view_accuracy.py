"""
Dashboard View 4: Random Forest Accuracy Assessment, Independent Google Earth Validation & Sanity Checks.
"""
import streamlit as st
import pandas as pd
from pipeline.sanity_checker import run_all_sanity_checks
from pipeline.validation import evaluate_independent_validation


def render_accuracy_view(datasets, city, season):
    st.subheader(f"View 4: RF Accuracy Assessment, Independent Validation & Sanity Checks — {city}")
    acc_df = datasets["accuracy"]

    st.markdown("#### 1. Automated Step-2 Pipeline Sanity Checks")
    checks = run_all_sanity_checks("data")
    check_df = pd.DataFrame(checks)
    st.table(check_df)

    st.markdown("#### 2. Independent Ground-Truth Validation (160 Stratified Google Earth Points)")
    val_res = evaluate_independent_validation("data/validation_points_google_earth.csv", city_filter="All")
    val_city = evaluate_independent_validation("data/validation_points_google_earth.csv", city_filter=city)

    col1, col2, col3 = st.columns(3)
    col1.metric("Headline Independent Overall Accuracy", f"{val_res['overall_accuracy']*100:.2f}%", f"n = {val_res['n_points']} points")
    col2.metric("Headline Independent Cohen's Kappa (κ)", f"{val_res['kappa']:.4f}", "Strong Agreement (>0.80)")
    col3.metric(f"{city} Subset Accuracy", f"{val_city['overall_accuracy']*100:.2f}%", f"κ = {val_city['kappa']:.4f}")

    st.markdown(f"##### Per-Class Producer's & User's Accuracy ({city})")
    st.dataframe(val_city["per_class_metrics"], use_container_width=True)

    st.markdown("#### 3. Multi-Year GEE Holdout & 2020 Cross-Year Accuracy (`accuracy.csv`)")
    sub_acc = acc_df[(acc_df["city"] == city) & (acc_df["season"] == season)]
    st.dataframe(sub_acc, use_container_width=True)
