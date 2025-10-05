import unittest

import numpy as np
import pandas as pd

from scripts.functions.data_manipulation_functions import apply_dilution_factor


class TestApplyDilutionFactor(unittest.TestCase):
    def test_applies_dilution_and_drops_it(self):
        test_df = pd.DataFrame({
            'non_data_col': ['a', 'b', 'c', 'd'],
            'dilution_factor': [2, 3, 4, 5],
            'target_col': [1.0, 2.0, 3.0, 4.0],
            'empty_col': [15.0, 1.0, np.nan, np.nan],
            'nontarget_col': [10.0, 20.0, 30.0, 40.0]
        })
        expected_df = pd.DataFrame({
            'non_data_col': ['a', 'b', 'c', 'd'],
            'target_col': [2.0, 6.0, 12.0, 20.0],
            'empty_col': [30.0, 3.0, np.nan, np.nan],
            'nontarget_col': [10.0, 20.0, 30.0, 40.0]
        })

        result_df = apply_dilution_factor(
            df=test_df,
            multiplier_col='dilution_factor',
            target_cols=['target_col', "empty_col"]
        )
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_emtpy_dilution_factor(self):
        test_df = pd.DataFrame({
            'non_data_col': ['a', 'b', 'c', 'd'],
            'empty_dilution_fact': [np.nan, np.nan, 2.0, 3.0],
            'target_col': [1.0, 2.0, 3.0, 4.0],
            'empty_col': [15.0, 1.0, np.nan, np.nan],
            'nontarget_col': [10.0, 20.0, 30.0, 40.0]
        })
        expected_df = pd.DataFrame({
            'non_data_col': ['a', 'b', 'c', 'd'],
            'target_col': [1.0, 2.0, 6.0, 12.0],
            'empty_col': [15.0, 1.0, np.nan, np.nan],
            'nontarget_col': [10.0, 20.0, 30.0, 40.0]
        })
        result_df = apply_dilution_factor(
            df=test_df,
            multiplier_col='empty_dilution_fact',
            target_cols=['target_col', "empty_col"]
        )
        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == '__main__':
    unittest.main()
