# tests.py

import os
from pathlib import Path
import unittest

from functions.get_files_info import MAX_CHARS, get_file_contents, get_files_info


class TestGetFilesInfo(unittest.TestCase):

    dir_calculator: str

    def setUp(self):
        wd = os.getcwd()
        self.dir_calculator = str(Path(wd) / "calculator")

    def test_root(self):
        # expect to get a list of files (a string with no Error keyword)
        result = get_files_info(self.dir_calculator, ".")
        self.assertNotIn("Error", result, "Expected no error in the result")

    def test_pkg(self):
        # expect to get a list of files (a string with no Error keyword)
        result = get_files_info(self.dir_calculator, "pkg")
        self.assertNotIn("Error", result, "Expected no error in the result")

    def test_bin(self):
        # Expects a str with the Keyword Error: at the front
        result = get_files_info(self.dir_calculator, "/bin")
        self.assertTrue(
            result.startswith("Error:"), "Expected result to start with 'Error:'"
        )

    def test_outside(self):
        # Expects a str with the Keyword Error: at the front
        result = get_files_info(self.dir_calculator, "../")
        self.assertTrue(
            result.startswith("Error:"), "Expected result to start with 'Error:'"
        )

    def test_lorem(self):
        # Expects a str with the Keyword Error: at the front
        result = get_file_contents(self.dir_calculator, "lorem.txt")
        self.assertNotIn("Error", result, "Expected no error in the result")
        self.assertLessEqual(
            len(result), MAX_CHARS, f"The result was not truncated to {MAX_CHARS}"
        )


if __name__ == "__main__":
    unittest.main()
