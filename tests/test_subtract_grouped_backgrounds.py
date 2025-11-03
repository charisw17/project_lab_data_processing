import unittest
import pandas as pd
from resources.constants_and_factors import WT, STERILE
from scripts.functions.data_manipulation_functions import subtract_grouped_background_from_data
from resources.path_util import PATH_TEST_DATA


class TestSubtractGroupedBackgroundsFromData(unittest.TestCase):

    def test_valid_background_and_data_as_hardcoded_input(self):
        test_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "bg_col": ["bg1", "bg1", "bg2", "bg2"],
            "col_1": [1.0, 3.0, 6.0, 4.0],
            "col_2": [10.0, 30.0, 60.0, 40.0],
            "col_3": [100.0, 300.0, 600.0, 400.0],
        })

        background_df = pd.DataFrame({
            "non_data_col": [STERILE, WT, WT],
            "bg_col": ["sterile", "bg1", "bg2"],
            "col_1": [0.1, 1, 2],
            "col_2": [0.5, 5, 10],
            "col_3": [0.3, 3, 30]
        })

        expected_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "bg_col": ["bg1", "bg1", "bg2", "bg2"],
            "col_1": [1.0, 3.0, 6.0, 4.0],
            "col_2": [5, 25.0, 50.0, 30.0],
            "col_3": [97, 297.0, 570.0, 370.0],
        })

        result = subtract_grouped_background_from_data(
            background_data_df=background_df,
            data_df=test_data_df,
            group_by_col= "bg_col",
            affected_columns=["col_2", "col_3"]
        )

        pd.testing.assert_frame_equal(result, expected_data_df)

    def test_valid_background_and_data_as_external_input(self):
        self.wt_mean = pd.read_excel(PATH_TEST_DATA / "wt_mean.xlsx")
        self.data_in = pd.read_excel(PATH_TEST_DATA / "data_in.xlsx")
        self.expected_out_df = pd.read_excel(PATH_TEST_DATA / "expected_out.xlsx")

        result = subtract_grouped_background_from_data(
            background_data_df=self.wt_mean,
            data_df=self.data_in,
            group_by_col= "bg_col",
            affected_columns=["col_2", "col_3"]
        )

        pd.testing.assert_frame_equal(result, self.expected_out_df)

if __name__ == '__main__':
    unittest.main()
