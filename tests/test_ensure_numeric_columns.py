import unittest

import pandas as pd

from scripts.functions.data_validation_functions import ensure_columns_are_numeric_type


class TestAllDataColumnsAreNumeric(unittest.TestCase):
    def test_supply_with_numeric_data(self):
        test_data = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c', 'd'],
            "numeric_col_1": [1.0, 2.0, 3.0, 4.0],
            "numeric_col_2": [5.0, 6.0, 7.0, 8.0]
        })
        result = ensure_columns_are_numeric_type(test_data, ["numeric_col_1", "numeric_col_2"])

        # Assert columns are numeric type
        self.assertTrue(pd.api.types.is_numeric_dtype(result["numeric_col_1"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(result["numeric_col_2"]))
        # Assert values are unchanged
        pd.testing.assert_frame_equal(result, test_data)

    def test_convert_string_numbers_to_numeric(self):
        test_data = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c'],
            "string_numbers": ['1.5', '2.0', '3.7']
        })
        result = ensure_columns_are_numeric_type(test_data, ["string_numbers"])
        expected_result = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c'],
            "string_numbers": [1.5, 2.0, 3.7]})

        self.assertTrue(pd.api.types.is_numeric_dtype(result["string_numbers"]))
        pd.testing.assert_frame_equal(result, expected_result)

    def test_raise_error_on_non_numeric_data(self):
        test_data = pd.DataFrame({
            "non_data_col": ['a', 'b', 'c'],
            "numeric_col_1": [1.0, 2.0, 3.0],
            "mixed_col": [1.0, 'String', 3.0]
        })
        with self.assertRaises(ValueError):
            ensure_columns_are_numeric_type(test_data, ["numeric_col_1", "mixed_col"])


if __name__ == '__main__':
    unittest.main()
