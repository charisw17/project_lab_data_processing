import numpy as np

from resources.constants_and_factors import COMPOUND_COEFFS, Compound, MG_TO_UG_FACTOR, PATHLENGTH, LIN_REG_D_BN, \
    LIN_REG_K_BN
from scripts.Extract_purity_calibration_curve import BETANIN_PURITY_FACTOR

def calc_rfu_per_od(df, rfu_col: str, od_col: str):
    zero_check = df[od_col].eq(0.0)
    if zero_check.any():
        raise ZeroDivisionError("OD column contains zero values, which would lead to division by zero.")
    return df[rfu_col] / df[od_col]


def calc_conc_via_abs(df, abs_col: str, od_col: str, compound: Compound):
    ext_coeff, mw = COMPOUND_COEFFS[compound]
    return (df[abs_col] * mw * MG_TO_UG_FACTOR) / (ext_coeff * PATHLENGTH * df[od_col])


def calc_conc_via_rfu(df, rfu_col: str, od_col: str):
    zero_check = df[od_col].eq(0.0)
    if zero_check.any():
        raise ZeroDivisionError("OD column contains zero values, which would lead to division by zero.")
    return ((df[rfu_col] - LIN_REG_D_BN) * BETANIN_PURITY_FACTOR) / (LIN_REG_K_BN * df[od_col])


def remove_outliers_iqr_nan(data):
    if len(data) < 4:
        return data.copy()

    q1 = np.nanpercentile(data, 25)
    q3 = np.nanpercentile(data, 75)
    iqr_1p5 = (q3 - q1) * 1.5

    lower_bound = q1 - iqr_1p5
    upper_bound = q3 + iqr_1p5

    outside_acceptable_range_mask = (data < lower_bound) | (data > upper_bound)  # | = or
    corrected_data = data.copy()
    corrected_data[outside_acceptable_range_mask] = np.nan
    return corrected_data
