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


def sample_dataframe() -> pd.DataFrame:
    segment_profiles = [
        ("Routine Loyalists", 20, 28, 30000, 50000, 75, 95, 10, 16, 13),
        ("Glow Starters", 28, 40, 60000, 85000, 45, 65, 6, 11, 12),
        ("Premium Skin Investors", 25, 35, 50000, 70000, 60, 80, 8, 13, 13),
        ("Community Trend Setters", 35, 50, 85000, 110000, 25, 45, 3, 8, 12),
    ]

    rows = []
    customer_id = 1001
    for _, age_min, age_max, income_min, income_max, spend_min, spend_max, freq_min, freq_max, count in segment_profiles:
        for idx in range(count):
            age_span = age_max - age_min
            income_span = income_max - income_min
            spend_span = spend_max - spend_min
            freq_span = freq_max - freq_min
            rows.append(
                {
                    "customer_id": customer_id,
                    "age": age_min + ((idx * 2 + customer_id) % (age_span + 1)),
                    "annual_income": income_min + ((idx * 3300 + customer_id * 97) % (income_span + 1)),
                    "spending_score": spend_min + ((idx * 3 + customer_id) % (spend_span + 1)),
                    "purchase_frequency": freq_min + ((idx + customer_id) % (freq_span + 1)),
                }
            )
            customer_id += 1

    return pd.DataFrame(rows)
