import unittest

import pandas as pd

from scripts.functions.data_manipulation_functions import apply_func_to_all_target_columns


def func_to_apply(data: pd.Series) -> pd.Series:
    return data * 2


class TestApplyToAllTargetCols(unittest.TestCase):

    def setUp(self):
        self.abs_col = "abs_col"
        self.od_col = "od_col"
        self.unrelated_col = "unrelated_col"

        self.test_df = pd.DataFrame({
            self.unrelated_col: [2.0, 3.0, 4.0, 5.0],
            self.abs_col: [1.0, 3.0, 6.0, 4.0],
            self.od_col: [0.1, 0.2, 0.3, 0.4],
        })

        self.target_columns = [self.abs_col, self.od_col]

    def test_applies_func_as_expected(self):
        expected = pd.DataFrame({
            self.unrelated_col: [2.0, 3.0, 4.0, 5.0],
            self.abs_col: [2.0, 6.0, 12.0, 8.0],
            self.od_col: [0.2, 0.4, 0.6, 0.8],
        })

        result = apply_func_to_all_target_columns(self.test_df, func_to_apply, self.target_columns)
        pd.testing.assert_frame_equal(result, expected)


if __name__ == '__main__':
    unittest.main()
