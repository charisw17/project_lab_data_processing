import unittest

import pandas as pd

from scripts.functions.data_validation_functions import replace_overflow_with_max


class TestReplaceOverflowWithMax(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            'col1': [1.0, 2.0, 'OVRFLW', 4.0],
            'col2': ['OVRFLW', 5.0, 6.0, 'OVRFLW'],
            'col3': [7.0, 8.0, 9.0, 'OVRFLW'],
            'non_data_col': ['a', 'b', 'c', 'OVRFLW']
        }
        self.df = pd.DataFrame(self.test_data)

    def test_replace_overflow_single_column(self):
        result = replace_overflow_with_max(self.df.copy(), ['col1', 'col2'], max_value=666)
        expected_df = pd.DataFrame({
            'col1': [1.0, 2.0, 666.0, 4.0],
            'col2': [666.0, 5.0, 6.0, 666.0],
            'col3': [7.0, 8.0, 9.0, 'OVRFLW'],
            'non_data_col': ['a', 'b', 'c', 'OVRFLW']
        })
        pd.testing.assert_frame_equal(result, expected_df)


if __name__ == '__main__':
    unittest.main()
