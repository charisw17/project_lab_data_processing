import unittest

import numpy as np
import pandas as pd

from scripts.functions.data_manipulation_functions import split_df_by_determinant_column, combine_split_dfs


class TestSplitDfByDeterminantAndCombine(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'determinant_col': ['a', 'a', 'b', 'c', 'a', 'b'],
            'data_1': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            'data_2': [1, np.nan, 3, np.nan, 5.0, 4.0],
        }
        self.df = pd.DataFrame(self.test_data)

    def test_splits_rows_as_expected(self):
        result = split_df_by_determinant_column(self.df, 'determinant_col')
        expected_data = {
            'a': pd.DataFrame({
                'determinant_col': ['a', 'a', 'a'],
                'data_1': [1.0, 2.0, 5.0],
                'data_2': [1, np.nan, 5.0]
            }, index=[0, 1, 4]),
            'b': pd.DataFrame({
                'determinant_col': ['b', 'b'],
                'data_1': [3.0, 6.0],
                'data_2': [3, 4.0]
            }, index=[2, 5]),
            'c': pd.DataFrame({
                'determinant_col': ['c'],
                'data_1': [4.0],
                'data_2': [np.nan]
            }, index=[3])
        }
        for category, expected_df in expected_data.items():
            pd.testing.assert_frame_equal(result[category], expected_df)

    def test_raises_if_determinant_col_not_in_df(self):
        with self.assertRaises(ValueError):
            split_df_by_determinant_column(self.df, 'non_existent_col')

    def test_combining_a_split_df_returns_the_original_df(self):
        result = split_df_by_determinant_column(self.df, 'determinant_col')
        combined_df = combine_split_dfs(result)
        pd.testing.assert_frame_equal(combined_df, self.df)


if __name__ == '__main__':
    unittest.main()
