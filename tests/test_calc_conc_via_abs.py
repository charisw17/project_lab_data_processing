import unittest

import pandas as pd

from resources.constants_and_factors import Compound
from scripts.functions.data_analysis_functions import calc_conc_via_abs


class TestCalculateConcentrationViaAbs(unittest.TestCase):

    def test_abs_col_contains_invalid_values_raises_error(self):
        test_data = {
            'invalid_col': [1.0, "this is not a number", 5.0, 4.0],
            'valid_col': [0.1, 0.2, 0.3, 0.4],
        }
        df = pd.DataFrame(test_data)
        with self.assertRaises(TypeError):
            calc_conc_via_abs(df, 'invalid_col', 'valid_col', Compound.BETALAMIC_ACID)
        with self.assertRaises(TypeError):
            calc_conc_via_abs(df, 'valid_col', 'invalid_col', Compound.BETALAMIC_ACID)

    def test_abs_or_od_supplied_with_non_corresponding_col_name(self):
        abs_col = "abs_col"
        od_col = "od_col"

        test_data = {
            abs_col: [1.0, 2.0, 5.0, 4.0],
            od_col: [0.1, 0.2, 0.3, 0.4],
        }
        df = pd.DataFrame(test_data)

        with self.assertRaises(KeyError):
            calc_conc_via_abs(df, "This col name does not exist", od_col, Compound.BETANIDIN)

        with self.assertRaises(KeyError):
            calc_conc_via_abs(df, abs_col, "This col name does not exist", Compound.BETANIDIN)

    def test_abs_and_od_supplied_with_valid_data(self):
        abs_col = "abs_col"
        od_col = "od_col"
        non_data_col = "non_data_col"

        test_df = pd.DataFrame({
            non_data_col: ['a', 'b', 'c', 'd'],
            abs_col: [1.0, 3.0, 6.0, 4.0],
            od_col: [0.1, 0.2, 0.3, 0.4],
        })

        expected_series = pd.Series(
            [142.579643, 213.869464, 285.159285, 142.579643])

        result = calc_conc_via_abs(test_df, abs_col, od_col, Compound.BETANINE)
        pd.testing.assert_series_equal(result, expected_series)


if __name__ == '__main__':
    unittest.main()
