import unittest

from resources.path_util import sanitize_filename


class TestSanitizeFilenamesFromUnsafeCharacters(unittest.TestCase):
    def test_replaces_space_with_underscore(self):
        input_name = "test file name with spaces"
        expected_output = "test_file_name_with_spaces"
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected_output)  # add assertion here
        pass

    def test_micro_to_u_replacement(self):
        input_name = "Concentration in Cellsuspension [µg/mL]"
        expected = "Concentration_in_Cellsuspension_ugmL"
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected)

    def test_allowed_characters_preserved(self):
        input_name = "valid_file-name.txt"
        expected = "valid_file-name.txt"
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected)

    def test_empty_string_returns_empty(self):
        input_name = ""
        expected = ""
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected)

    def test_only_special_characters(self):
        input_name = "[@#$%^&*()]"
        expected = ""
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected)

    def test_numbers_preserved(self):
        input_name = "data_file_123.csv"
        expected = "data_file_123.csv"
        result = sanitize_filename(input_name)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
