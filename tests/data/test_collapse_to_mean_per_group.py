import unittest
from scripts.functions.data_manipulation_functions import collapse_to_means_per_group
import pandas as pd


class TestCollapseToMeanPerGroup(unittest.TestCase):
    def setUp(self):

        self.test_data_df = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "name": ["bg1_wt", "bg1_wt", "bg2_wt", "bg2_wt"],
            "bg_col": ["bg1", "bg1", "bg2", "bg2"],
            "col_1": [1.0, 3.0, 4.0, 7.0],
            "col_2": [10.0, 30.0, 40.0, 70.0],
            "col_3": [100.0, 300.0, 400.0, 700.0],
        })

    def    test_collapse_to_means_per_group(self):
        expected_data_df = pd.DataFrame({
            "non_data_col": ['a', 'c'],
            "name": ["bg1_wt", "bg2_wt"],
            "bg_col": ["bg1", "bg2"],
            "col_1": [2, 5.5],
            "col_2": [20, 55.0],
            "col_3": [200, 550.0],
        })

        result = collapse_to_means_per_group(
            df= self.test_data_df,
            group_by_col=["bg_col"],
        )

        pd.testing.assert_frame_equal(result, expected_data_df)


if __name__ == '__main__':
    unittest.main()
