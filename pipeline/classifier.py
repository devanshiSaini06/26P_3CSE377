"""
Patched v2 Random Forest Classifier & Temporal Post-Processing Module.
Fixes the v1 single-year retraining instability by:
  1. Training ONE Random Forest classifier per city & season anchored on 2021 reference labels.
  2. Applying the fixed classifier consistently across all years (2018-2026).
  3. Applying a 3-year sliding temporal majority filter to suppress single-year spectral noise.
  4. Enforcing a physical 'built-up non-reversion' rule (once urban built-up, does not revert).
  5. Running a 2021 hold-out accuracy evaluation AND a 2020 cross-year accuracy check.
"""
import numpy as np
from pipeline.config import FEATURE_BANDS, WORLDCOVER_COLLECTION


def generate_reference_labels_gee(composite_img):
    """
    Builds multi-index + ESA WorldCover 2021 guided reference label image:
      0 = Built-up, 1 = Water, 2 = Vegetation, 3 = Barren
    """
    import ee

    worldcover = ee.ImageCollection(WORLDCOVER_COLLECTION).first()
    ndvi = composite_img.select("NDVI")
    mndwi = composite_img.select("MNDWI")
    ndbi = composite_img.select("NDBI")

    labels = ee.Image(3)  # Default: Barren (3)
    labels = labels.where(ndvi.gt(0.32).Or(worldcover.eq(10)).Or(worldcover.eq(30)), 2)
    labels = labels.where(
        worldcover.eq(50).Or(ndbi.gt(0.05).And(ndvi.lt(0.22)).And(mndwi.lt(-0.05))), 0
    )
    labels = labels.where(worldcover.eq(80).Or(mndwi.gt(0.05).And(ndvi.lt(0.25))), 1)
    return labels.rename("class").toByte()


def train_fixed_2021_classifier_gee(composite_2021, roi, num_trees=100, points_per_class=600):
    """
    Trains a smileRandomForest classifier on 2021 composite + reference labels
    and evaluates holdout accuracy.
    """
    import ee

    labels_2021 = generate_reference_labels_gee(composite_2021)
    training_stack = composite_2021.select(FEATURE_BANDS).addBands(labels_2021)

    samples = training_stack.stratifiedSample(
        numPoints=points_per_class,
        classBand="class",
        region=roi,
        scale=10,
        seed=42,
        geometries=False,
    )

    with_random = samples.randomColumn("rand", 42)
    train_set = with_random.filter(ee.Filter.lt("rand", 0.8))
    val_set = with_random.filter(ee.Filter.gte("rand", 0.8))

    classifier = ee.Classifier.smileRandomForest(numberOfTrees=num_trees, seed=42).train(
        features=train_set,
        classProperty="class",
        inputProperties=FEATURE_BANDS,
    )

    val_classified = val_set.classify(classifier)
    conf_matrix = val_classified.errorMatrix("class", "classification")
    oa = float(conf_matrix.accuracy().getInfo())
    kappa = float(conf_matrix.kappa().getInfo())

    return classifier, oa, kappa


def evaluate_cross_year_2020_gee(classifier, composite_2020, roi, points_per_class=300):
    """
    Evaluates the 2021-trained Random Forest classifier on 2020 reference labels
    to verify temporal transferability (Step 1 Fix verification).
    """
    import ee

    labels_2020 = generate_reference_labels_gee(composite_2020)
    eval_stack = composite_2020.select(FEATURE_BANDS).addBands(labels_2020)
    eval_samples = eval_stack.stratifiedSample(
        numPoints=points_per_class,
        classBand="class",
        region=roi,
        scale=10,
        seed=2020,
        geometries=False,
    )
    classified_2020 = eval_samples.classify(classifier)
    conf_matrix = classified_2020.errorMatrix("class", "classification")
    oa = float(conf_matrix.accuracy().getInfo())
    kappa = float(conf_matrix.kappa().getInfo())
    return oa, kappa


def apply_temporal_filter_and_non_reversion_numpy(yearly_matrices):
    """
    Local 2D NumPy implementation of the Patched v2 post-processing rules:
      1. 3-year sliding window majority (mode) filter across time.
      2. Built-up non-reversion rule: once a pixel is classified as Built-up (0),
         it remains Built-up (0) in subsequent years.
    Parameters:
      yearly_matrices: list of 2D numpy integer arrays (H x W) ordered from 2018 to 2026.
    Returns:
      smoothed_matrices: list of 2D numpy integer arrays (H x W) of the same length.
    """
    stack = np.asarray(yearly_matrices, dtype=np.int32)  # Shape: (T, H, W)
    num_years, h, w = stack.shape
    majority_filtered = np.zeros_like(stack)

    for t in range(num_years):
        t_prev = max(0, t - 1)
        t_next = min(num_years - 1, t + 1)
        window = stack[[t_prev, t, t_next], :, :]  # Shape: (3, H, W)

        # Compute pixel-wise mode across the 3-year window
        # If all 3 years disagree, keep center year t
        c0, c1, c2 = window[0], window[1], window[2]
        mode_map = np.where(c0 == c1, c0, np.where(c1 == c2, c1, np.where(c0 == c2, c0, c1)))
        majority_filtered[t] = mode_map

    # Apply Built-up (class 0) non-reversion rule cumulatively from t=0..T-1
    smoothed = np.copy(majority_filtered)
    built_up_accum = (smoothed[0] == 0)
    for t in range(1, num_years):
        built_up_accum = np.logical_or(built_up_accum, smoothed[t] == 0)
        smoothed[t] = np.where(built_up_accum, 0, smoothed[t])

    return [smoothed[t] for t in range(num_years)]
