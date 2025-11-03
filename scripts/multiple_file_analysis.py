from resources.constants_and_factors import *
from resources.path_util import *
from scripts.functions.data_analysis_functions import calc_conc_via_abs, calc_conc_via_rfu, calc_rfu_per_od
from scripts.functions.data_analysis_functions import remove_outliers_iqr_nan
from scripts.functions.data_manipulation_functions import apply_func_to_all_target_columns, \
    split_df_by_determinant_column, combine_split_dfs, subtract_grouped_background_from_data, \
    collapse_to_means_per_group
from scripts.functions.data_manipulation_functions import create_df_subset, \
    collapse_df_to_means, subtract_background_from_data, apply_dilution_factor, filter_out_by_threshold, \
    ComparisonFuncType
from scripts.functions.data_validation_functions import replace_overflow_with_max, \
    ensure_columns_are_numeric_type

for path in [PATH_DATA_OUT]:
    if not os.path.exists(path):
        os.makedirs(path)

## Load data from excel or csv file
raw_data_df = load_df_from_excel(PATH_DATA_IN / "20240807_pCW001-3_Rescreening.xlsx")
show_or_store_df(raw_data_df, "raw_data_df.xlsx")

# DATA VALIDATION
## Replace "OVRFLW" with the value 100 000 (measurement maximum).
raw_data_ovrflow_rem_df = replace_overflow_with_max(raw_data_df, all_data_cols)
show_or_store_df(raw_data_ovrflow_rem_df, "raw_data_ovrflow_rem_df.xlsx")

## Ensure that all data columns are of type float
raw_data_ovrflow_rem_floats_df = ensure_columns_are_numeric_type(raw_data_ovrflow_rem_df, all_data_cols)
show_or_store_df(raw_data_ovrflow_rem_floats_df, "raw_data_ovrflow_rem_floats_df.xlsx")

# COLLECT BACKGROUND DATA:
## Create Dataframe consisting of only the sterile control
sterile_subset_df = create_df_subset(NAME, STERILE, raw_data_ovrflow_rem_floats_df, metadata_cols + all_data_cols)
show_or_store_df(sterile_subset_df, "sterile_subset_df.xlsx")

## Remove contaminated wells i.e. where cell density above 0.1, keep only clean wells.
sterile_subset_filtered_df = filter_out_by_threshold(
    df=sterile_subset_df,
    determinant_column_name=CELLSUSP_OD,
    affected_column_names=all_data_cols,
    comparison_type=ComparisonFuncType.GREATER_EQUAL,
    threshold=PLATE_READER_THRESHOLD)

sterile_subset_filtered_df = filter_out_by_threshold(
    df=sterile_subset_filtered_df,
    determinant_column_name=SUP_OD,
    affected_column_names=sup_data_cols,
    comparison_type=ComparisonFuncType.GREATER_EQUAL,
    threshold=PLATE_READER_THRESHOLD)
show_or_store_df(sterile_subset_filtered_df, "sterile_subset_filtered_df.xlsx")

## Create Dataframe consisting of only the means of the sterile ctrl
sterile_subset_means_df = collapse_df_to_means(sterile_subset_filtered_df)
show_or_store_df(sterile_subset_means_df, "sterile_subset_means_df.xlsx")

# PREPARE DATA FOR ANALYSIS:
## Create separate Dataframes for Cellsuspension and Supernatant data (excl. sterile controls) so they can be processed separately and outliers in one sample type do not affect the other.
data_subset_df = create_df_subset(
    column_name=NAME,
    search_word=STERILE,
    df=raw_data_ovrflow_rem_floats_df,
    selected_columns=metadata_cols + all_data_cols,
    invert=True)
show_or_store_df(data_subset_df, "data_subset_df.xlsx")

## Filter out invalid measurements: remove empty cellsuspension measurements (ie. OD < 0.1) and contaminated supernatant measurements (ie. OD >= 0.1) by replacing them with NaN.
data_filtered_df = filter_out_by_threshold(
    df=data_subset_df,
    determinant_column_name=CELLSUSP_OD,
    affected_column_names=cellsusp_data_cols,
    comparison_type=ComparisonFuncType.LESS_THAN,
    threshold=PLATE_READER_THRESHOLD
)

data_filtered_df = filter_out_by_threshold(
    df=data_filtered_df,
    determinant_column_name=SUP_OD,
    affected_column_names=sup_data_cols,
    comparison_type=ComparisonFuncType.GREATER_EQUAL,
    threshold=PLATE_READER_THRESHOLD
)
show_or_store_df(data_filtered_df, "data_filtered_df.xlsx")

# ## Collect WT background data for grouped background subtraction
# wt_subset_df = create_df_subset(NAME, r"_WT$", data_filtered_df, metadata_cols + all_data_cols)
# show_or_store_df(wt_subset_df, "wt_subset_df.xlsx")
#
# wt_subset_means_df = collapse_to_means_per_group(
#     df= wt_subset_df,
#     group_by_col= WT
# )
# show_or_store_df(wt_subset_means_df, "wt_subset_means_df.xlsx")

# ## Remove background signal: subtract WILDTYPE means from RFU data columns
# data_background_rfu_corrected_df = subtract_grouped_background_from_data(
#     background_data_df=wt_subset_means_df,
#     data_df=data_filtered_df,
#     group_by_col= WT,
#     affected_columns=cellsusp_rfu_data_cols + sup_rfu_data_cols)

## Remove background signal: subtract STERILE means from ABSORBANCE data columns
data_background_abs_corrected_df = subtract_background_from_data(
    background_data_row=sterile_subset_means_df,
    data_df=data_filtered_df,
    affected_columns=cellsusp_abs_data_cols + sup_abs_data_cols
)
show_or_store_df(data_background_abs_corrected_df, "data_background_abs_corrected_df.xlsx")


# todo: possibly move apply dilution factor somewhere else?

## Apply dilution factor: multiply data cols with the corresponding dilution factor.
data_background_and_dilution_corrected_df = apply_dilution_factor(
    df=data_background_abs_corrected_df,
    multiplier_col=CELLSUSP_DF,
    target_cols=cellsusp_data_cols, )

data_background_and_dilution_corrected_df = apply_dilution_factor(
    df=data_background_and_dilution_corrected_df,
    multiplier_col=SUP_DF,
    target_cols=sup_data_cols, )

show_or_store_df(data_background_and_dilution_corrected_df, "data_background_and_dilution_corrected_df.xlsx")



# CALCULATE CONCENTRATIONS:
## Absorbance via Lambert Beer: Extinction coefficient e [L/(mol*cm)], Molecular Weight MW [g/ml], pathlength p [cm]
calculated_concentrations_df = data_background_and_dilution_corrected_df[metadata_cols].copy()

calculated_concentrations_df[C_ABS_Cellsusp_Bl] = calc_conc_via_abs(
    df=data_background_and_dilution_corrected_df,
    abs_col=CELLSUSP_ABS_Bl,
    od_col=CELLSUSP_OD,
    compound=Compound.BETALAMIC_ACID
)

calculated_concentrations_df[C_ABS_Sup_Bn] = calc_conc_via_abs(
    df=data_background_and_dilution_corrected_df,
    abs_col=SUP_ABS_Bn,
    od_col=CELLSUSP_OD,
    compound=Compound.BETANINE
)

calculated_concentrations_df[C_ABS_Sup_Bl] = calc_conc_via_abs(
    df=data_background_and_dilution_corrected_df,
    abs_col=SUP_ABS_Bl,
    od_col=CELLSUSP_OD,
    compound=Compound.BETALAMIC_ACID
)

## Fluorescence via Calibration Curve: x = (y-d)/k [µg/mL]
calculated_concentrations_df[C_RFU_Cellsusp_Bn] = calc_conc_via_rfu(
    df=data_background_and_dilution_corrected_df,
    rfu_col=CELLSUSP_RFU_Bn,
    od_col=CELLSUSP_OD,
)
calculated_concentrations_df[C_RFU_Sup_Bn] = calc_conc_via_rfu(
    df=data_background_and_dilution_corrected_df,
    rfu_col=SUP_RFU_Bn,
    od_col=CELLSUSP_OD,
)

# CALCULATE RFU/OD:
calculated_concentrations_df[RFUperOD_Cellsusp_Bn] = calc_rfu_per_od(
    df=data_background_and_dilution_corrected_df,
    rfu_col=CELLSUSP_RFU_Bn,
    od_col=CELLSUSP_OD
)

show_or_store_df(calculated_concentrations_df, "calculated_concentrations_df.xlsx")

## Collect WT background for grouped background subtraction
wt_subset_df = create_df_subset(
    column_name=NAME,
    search_word=r"_WT$",
    df=calculated_concentrations_df,
    selected_columns=metadata_cols + CONCENTRATION_RESULT_COLS)
show_or_store_df(wt_subset_df, "wt_subset_df.xlsx")

wt_subset_means_df = collapse_to_means_per_group(
    df= wt_subset_df,
    group_by_col= WT
)
show_or_store_df(wt_subset_means_df, "wt_subset_means_df.xlsx")

## Remove background signal: subtract WILDTYPE means from RFU data columns
calc_conc_background_rfu_corrected_df = subtract_grouped_background_from_data(
    background_data_df=wt_subset_means_df,
    data_df=calculated_concentrations_df,
    group_by_col= WT,
    affected_columns=[C_RFU_Cellsusp_Bn, C_RFU_Sup_Bn, RFUperOD_Cellsusp_Bn])


# OUTLIER DETECTION AND REMOVAL
## Split DataFrame by NAME column to remove outliers for each strain separately via IQR method, then recombine the dataframes into one.
dfs_split_by_strain = split_df_by_determinant_column(
    df=calc_conc_background_rfu_corrected_df,
    determinant_col=NAME,
)

result_dfs_split_by_strain = {}
for name, df in dfs_split_by_strain.items():
    result_dfs_split_by_strain[name] = apply_func_to_all_target_columns(df, remove_outliers_iqr_nan,
                                                                        CONCENTRATION_RESULT_COLS)

outlier_removed_df = combine_split_dfs(result_dfs_split_by_strain)
show_or_store_df(outlier_removed_df, "result.xlsx")

