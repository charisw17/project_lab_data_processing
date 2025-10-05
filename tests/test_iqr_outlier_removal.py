import unittest

import numpy as np

from scripts.functions.data_analysis_functions import remove_outliers_iqr_nan


class TestIQROutlierRemoval(unittest.TestCase):
    def test_removes_severe_outlier_as_expected(self):
        data = np.array([29.16836250169584,
                         25.32022639261245,
                         40.02170668837336,
                         37.46521087561549,
                         169.9644850329782])

        result = remove_outliers_iqr_nan(data)

        expected_result = np.array([29.16836250169584,
                                    25.32022639261245,
                                    40.02170668837336,
                                    37.46521087561549,
                                    np.nan])

        self.assertTrue(np.allclose(result, expected_result, equal_nan=True))

    def test_ignores_np_nan(self):
        data = np.array([29.16836250169584,
                         25.32022639261245,
                         40.02170668837336,
                         37.46521087561549,
                         169.9644850329782,
                         np.nan,
                         np.nan,
                         np.nan])

        result = remove_outliers_iqr_nan(data)

        expected_result = np.array([29.16836250169584,
                                    25.32022639261245,
                                    40.02170668837336,
                                    37.46521087561549,
                                    np.nan,
                                    np.nan,
                                    np.nan,
                                    np.nan
                                    ])

        self.assertTrue(np.allclose(result, expected_result, equal_nan=True))

    def test_does_not_do_anything_for_less_than_4_data_points(self):
        data = np.array([29.16836250169584,
                         25.32022639261245,
                         40.02170668837336,
                         ])

        result = remove_outliers_iqr_nan(data)

        expected_result = np.array([29.16836250169584,
                                    25.32022639261245,
                                    40.02170668837336,
                                    ])

        self.assertTrue(np.allclose(result, expected_result, equal_nan=True))
