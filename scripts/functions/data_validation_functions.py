import pandas as pd


def replace_overflow_with_max(df, cols, max_value=100000):
    df = df.copy()
    df[cols] = df[cols].replace("OVRFLW", max_value).astype(float)
    return df


def replace_empty_string_with_nan(df, cols):
    df = df.copy()
    df[cols] = df[cols].replace(["", " "], pd.NA)
    return df


def replace_outliers_with_nan(df, column, threshold=3):  # TODO: Implement this function
    return df


def ensure_columns_are_numeric_type(df,
                                    cols):  # Ensures that specified columns in the DataFrame are numeric, converting them if necessary
    df = df.copy()
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='raise')
    return df
