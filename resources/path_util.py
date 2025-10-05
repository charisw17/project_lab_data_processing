import os
import re
from pathlib import Path

import pandas as pd


def path_to_project_root(project_name):
    path = os.getcwd()
    while not str(path).endswith(project_name):
        path = Path(path).parent

    return path


PROJECT_ROOT_NAME = 'dwp_data_processing_and_analysis'
PATH_ROOT_DIR = Path(path_to_project_root(PROJECT_ROOT_NAME))
PATH_DATA = PATH_ROOT_DIR / "data"
PATH_DATA_IN = PATH_DATA / "in"
PATH_DATA_OUT = PATH_DATA / "out"


def show_or_store_df(df, file_name, store_as_excel=True):
    if store_as_excel:
        df.to_excel(PATH_DATA_OUT / file_name, index=False)
    else:
        return df.head(20)


def load_df_from_csv(file_path):
    df = pd.read_csv(file_path, sep=",", header=0)
    return df


def load_df_from_excel(file_path):
    df = pd.read_excel(file_path, header=0)
    return df


def sanitize_filename(file_name: str) -> str:  # Replacing spaces with underscores and removing special characters.
    sanitized_name = file_name.replace(" ", "_")
    sanitized_name = sanitized_name.replace("µ", "u")
    sanitized_name = re.sub(r'[^\w\-_.]', '', sanitized_name)
    return sanitized_name
