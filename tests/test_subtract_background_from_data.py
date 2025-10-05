import unittest

import pandas as pd

from resources.constants_and_factors import STERILE
from scripts.functions.data_manipulation_functions import subtract_background_from_data


class TestSubtractBackgroundFromData(unittest.TestCase):
    def test_valid_background_and_data_as_input(self):
        test_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "col_1": [1.0, 3.0, 6.0, 4.0],
            "col_2": [10.0, 30.0, 60.0, 40.0],
            "col_3": [100.0, 300.0, 600.0, 400.0],
        })

        background_df = pd.DataFrame({
            "non_data_col": [STERILE],
            "col_1": [0.1],
            "col_2": [0.5],
        })

        expected_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "col_1": [0.9, 2.9, 5.9, 3.9],
            "col_2": [9.5, 29.5, 59.5, 39.5],
            "col_3": [100.0, 300.0, 600.0, 400.0],
        })

        result = subtract_background_from_data(
            background_data_row=background_df,
            data_df=test_data_df,
            affected_columns=["col_1", "col_2"]
        )

        pd.testing.assert_frame_equal(result, expected_data_df)

    def test_does_not_change_the_input_df(self):
        test_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "col_1": [1.0, 3.0, 6.0, 4.0],
            "col_2": [10.0, 30.0, 60.0, 40.0],
            "col_3": [100.0, 300.0, 600.0, 400.0],
        })

        background_df = pd.DataFrame({
            "non_data_col": [STERILE],
            "col_1": [0.1],
            "col_2": [0.5],
        })

        original_df = test_data_df.copy()
        subtract_background_from_data(
            background_data_row=background_df,
            data_df=test_data_df,
            affected_columns=["col_1", "col_2"]
        )
        pd.testing.assert_frame_equal(test_data_df, original_df)

    def test_background_multiple_rows_raises(self):
        test_data_df = pd.DataFrame({
            "col_1": [1.0, 3.0]})
        background_df = pd.DataFrame({
            "col_1": [0.1, 0.2]})

        with self.assertRaises(ValueError):
            subtract_background_from_data(background_df, test_data_df, ["col_1"])

    def test_empty_data_df(self):
        test_data_df = pd.DataFrame({
            "col_1": [],
            "col_2": []})

        background_df = pd.DataFrame({
            "col_1": [0.1],
            "col_2": [0.5]})

        result = subtract_background_from_data(
            background_data_row=background_df,
            data_df=test_data_df,
            affected_columns=["col_1", "col_2"])
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()
