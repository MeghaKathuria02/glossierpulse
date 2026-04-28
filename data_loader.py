import pandas as pd


# Keep only the columns we need for segmentation.
REQUIRED_COLUMNS = ["customer_id", "age", "annual_income", "spending_score", "purchase_frequency"]


def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean customer dataframe for analysis.
    """
    # Check that the CSV has all required columns.
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Expected columns: {REQUIRED_COLUMNS}"
        )

    # Keep only the required columns in a predictable order.
    df = df[REQUIRED_COLUMNS].copy()

    # Convert numeric fields to numbers; invalid values become NaN.
    numeric_columns = ["age", "annual_income", "spending_score", "purchase_frequency"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing customer id.
    df = df.dropna(subset=["customer_id"])

    # Fill missing numeric values using the median for each column.
    for col in numeric_columns:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)

    # Remove duplicate customer ids and keep the first record.
    df = df.drop_duplicates(subset=["customer_id"], keep="first")

    # Final reset so UI tables look clean.
    return df.reset_index(drop=True)


def load_and_clean_data(file) -> pd.DataFrame:
    """
    Load customer CSV data and clean it for analysis.
    """
    df = pd.read_csv(file)
    return clean_customer_data(df)
