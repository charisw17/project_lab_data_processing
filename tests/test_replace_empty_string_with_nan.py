import unittest

import pandas as pd

from scripts.functions.data_validation_functions import replace_empty_string_with_nan


class TestReplaceEmptyStringWithNaN(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            'col1': [1.0, 2.0, 'OVRFLW', 4.0],
            'col2': ['OVRFLW', 5.0, "", 'OVRFLW'],
            'col3': [7.0, " ", 9.0, 'OVRFLW'],
            'non_data_col': ['a', 'b', '', 'OVRFLW']
        }
        self.df = pd.DataFrame(self.test_data)

    def test_replace_empty_string_with_NaN(self):
        result = replace_empty_string_with_nan(self.df.copy(), ['col1', 'col2', "col3"])
        expected_data = {
            'col1': [1.0, 2.0, 'OVRFLW', 4.0],
            'col2': ['OVRFLW', 5.0, pd.NA, 'OVRFLW'],
            'col3': [7.0, pd.NA, 9.0, 'OVRFLW'],
            'non_data_col': ['a', 'b', '', 'OVRFLW']
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result, expected_df)


if __name__ == '__main__':
    unittest.main()
