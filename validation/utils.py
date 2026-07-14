import pandas as pd


def validation_summary(df: pd.DataFrame):
    """
    Returns a dictionary containing basic data quality metrics.
    """
    return {
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }