import unittest

import numpy as np
import pandas as pd

from resources.constants_and_factors import PLATE_READER_THRESHOLD
from scripts.functions.data_manipulation_functions import filter_out_by_threshold, ComparisonFuncType


class TestFilterByThreshold(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'non_data_col': ['a', 'b', 'c', 'd', 'e', 'f'],
            'valid_determinant': [0.001, 0.05, 0.1, 0.2, 2.0, 8.0],
            'invalid_determinant': [0.001, "String", 0.1, 0.2, "String", 8.0],
            'valid_affected': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            'invalid_affected': [1, np.nan, 3, np.nan, 5.0, 4.0],
            'non-affected': [10, "String", 330, np.nan, 0, -40.0]
        }
        self.df = pd.DataFrame(self.test_data)

    def test_valid_input(self):
        result = filter_out_by_threshold(
            df=self.df.copy(),
            determinant_column_name="valid_determinant",
            affected_column_names=["valid_affected", "invalid_affected"],
            comparison_type=ComparisonFuncType.LESS_THAN,
            threshold=PLATE_READER_THRESHOLD
        )

        expected_data = {
            'non_data_col': ['a', 'b', 'c', 'd', 'e', 'f'],
            'valid_determinant': [0.001, 0.05, 0.1, 0.2, 2.0, 8.0],
            'invalid_determinant': [0.001, "String", 0.1, 0.2, "String", 8.0],
            'valid_affected': [np.nan, np.nan, 3.0, 4.0, 5.0, 6.0],
            'invalid_affected': [np.nan, np.nan, 3, np.nan, 5.0, 4.0],
            'non-affected': [10, "String", 330, np.nan, 0, -40.0]

        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    def test_fail_if_determinant_or_affected_contain_non_numeric_data(self):
        with self.assertRaises(TypeError):
            filter_out_by_threshold(
                df=self.df.copy(),
                determinant_column_name="invalid_determinant",
                affected_column_names=["invalid_affected"],
                comparison_type=ComparisonFuncType.GREATER_EQUAL,
                threshold=0.1
            )


if __name__ == '__main__':
    unittest.main()
