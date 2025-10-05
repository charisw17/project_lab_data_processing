import enum
import operator
from typing import Callable

import numpy as np
import pandas as pd


def create_df_subset(column_name, search_word, df, selected_columns, invert=False):
    """Filters a Dataframe to only include (or exclude, if invert=True) rows where the specified column column_name contains the specified search_word"""
    mask = df[column_name].astype(str).str.contains(search_word, case=False, na=False)
    if invert:
        mask = ~mask
    df_subset = df[mask][selected_columns]
    return df_subset


class ComparisonFuncType(enum.Enum):
    GREATER_THAN = operator.gt
    GREATER_EQUAL = operator.ge
    LESS_THAN = operator.lt
    LESS_EQUAL = operator.le
    EQUAL = operator.eq


def apply_func_to_all_target_columns(df: pd.DataFrame, func: Callable[[pd.Series], pd.Series],
                                     target_columns: list[str]) -> pd.DataFrame:
    result_df = df.copy()
    for col in target_columns:
        result_df[col] = func(df[col])
    return result_df


def filter_out_by_threshold(df: pd.DataFrame, determinant_column_name: str, affected_column_names: list[str],
                            comparison_type: ComparisonFuncType, threshold: float) -> pd.DataFrame:
    columns_to_check = [determinant_column_name] + affected_column_names
    if not all(df[col].dtype == 'float64' for col in columns_to_check):
        raise TypeError(f"Columns {columns_to_check} must be of dtype float64.")

    compare_func = comparison_type.value
    mask = compare_func(pd.to_numeric(df[determinant_column_name], errors='coerce'), threshold)

    df_filtered = df.copy()
    df_filtered.loc[mask, affected_column_names] = np.nan
    return df_filtered


def collapse_df_to_means(df):
    """Collapses values in each numeric column in the given dataframe to their mean, while keeping the first line of strings in non-numeric columns as is. """
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    str_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    num_cols_df = pd.DataFrame([df[num_cols].mean()])
    str_cols_df = df[str_cols].iloc[[0]].reset_index(drop=True)

    result_df = pd.concat([str_cols_df, num_cols_df], axis=1)
    return result_df


def subtract_background_from_data(background_data_row, data_df, affected_columns):
    if background_data_row.shape[0] != 1:
        raise ValueError("background_data_row must contain exactly one row.")

    return data_df.assign(
        **{col: data_df[col] - background_data_row.iloc[0][col] for col in affected_columns}
    )


def apply_dilution_factor(df, multiplier_col, target_cols):
    df = df.copy()
    for col in target_cols:
        df[col] = df[col].where(df[multiplier_col].isna(),
                                df[col] * df[multiplier_col])
    df.drop(columns=[multiplier_col], inplace=True)
    return df


# TODO: Implement sort_data function
def sort_data(df, sort_by, ascending=True):
    # return df.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)
    pass


def split_df_by_determinant_column(df, determinant_col: str):
    if determinant_col not in df.columns:
        raise ValueError(f"Column '{determinant_col}' not found in DataFrame")

    category_dfs = {}
    for category in df[determinant_col].unique():
        category_dfs[category] = df[df[determinant_col] == category].copy()

    return category_dfs


def combine_split_dfs(split_dfs_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(split_dfs_dict.values(), ignore_index=False).sort_index()
