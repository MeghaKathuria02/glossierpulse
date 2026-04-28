import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = ["age", "annual_income", "spending_score", "purchase_frequency"]


def assign_segments(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Run K-Means and add a customer segment label to the dataframe.
    """
    missing_features = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing feature columns for clustering: {missing_features}")

    # Use only segmentation features.
    feature_data = df[FEATURE_COLUMNS].copy()

    # Scale features so one column does not dominate clustering.
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_data)

    # Fit K-Means model.
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_ids = model.fit_predict(scaled_features)

    segmented_df = df.copy()
    segmented_df["segment_id"] = cluster_ids
    segmented_df["segment_name"] = segmented_df["segment_id"].apply(get_segment_name)

    return segmented_df


def get_segment_name(segment_id: int) -> str:
    """
    Map numeric segment ids to beginner-friendly names.
    """
    name_map = {
        0: "Glow Starters",
        1: "Routine Loyalists",
        2: "Premium Skin Investors",
        3: "Community Trend Setters",
    }
    return name_map.get(segment_id, f"Segment {segment_id}")


def segment_summary(df_with_segments: pd.DataFrame) -> pd.DataFrame:
    """
    Build a quick per-segment summary table for the dashboard.
    """
    summary = (
        df_with_segments.groupby(["segment_id", "segment_name"], as_index=False)
        .agg(
            customers=("customer_id", "count"),
            avg_age=("age", "mean"),
            avg_income=("annual_income", "mean"),
            avg_spending=("spending_score", "mean"),
            avg_purchase_frequency=("purchase_frequency", "mean"),
        )
        .sort_values("segment_id")
    )
    return summary
