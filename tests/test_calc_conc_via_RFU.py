import unittest

import numpy as np
import pandas as pd

from scripts.functions.data_analysis_functions import calc_conc_via_rfu


class TestCalculateConcentrationViaRFU(unittest.TestCase):
    def test_abs_and_od_supplied_with_valid_data(self):
        non_data_col = "non_data_col"
        rfu_col = "rfu_col"
        od_col = "od_col"

        test_df = pd.DataFrame({
            non_data_col: ['a', 'b', 'c', 'd'],
            rfu_col: [1000.0, 3000.0, 6000.0, 4000.0],
            od_col: [0.1, 0.2, 0.3, 0.4],
        })

        expected_series = pd.Series(
            [1225.061728,
             4727.757202,
             7267.064472,
             3392.685185]
        )

        result = calc_conc_via_rfu(test_df, rfu_col, od_col)
        pd.testing.assert_series_equal(result, expected_series)

    def test_rfu_col_contains_invalid_values_raises_error(self):
        df = pd.DataFrame({
            'invalid_col': [1.0, "this is not a number", 5.0, 4.0],
            'valid_col': [0.1, 0.2, 0.3, 0.4],
        })
        with self.assertRaises(TypeError):
            calc_conc_via_rfu(df, 'invalid_col', 'valid_col')
        with self.assertRaises(TypeError):
            calc_conc_via_rfu(df, 'valid_col', 'invalid_col')

    def test_ignores_if_rfu_or_od_are_empty(self):
        test_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "rfu_col": [0.0, np.nan, 6000.0, 4000.0],
            "od_col": [0.1, 0.2, 0.3, np.nan],
        })

        expected_series = pd.Series(
            [-2890.164609,
             np.nan,
             7267.064472,
             np.nan, ])

        result = calc_conc_via_rfu(test_df, "rfu_col", "od_col")
        pd.testing.assert_series_equal(result, expected_series)

    def test_raises_if_od_contains_zero_values(self):
        test_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "rfu_col": [0.0, 3000.0, 6000.0, 4000.0],
            "od_col": [0.1, 0.2, 0.3, 0.0],
        })

        with self.assertRaises(ZeroDivisionError):
            calc_conc_via_rfu(test_df, "rfu_col", "od_col")


if __name__ == '__main__':
    unittest.main()
