# tests.py

import os
from pathlib import Path
import unittest

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):

    dir_calculator: str

    def setUp(self):
        wd = os.getcwd()
        self.dir_calculator = str(Path(wd) / "calculator")

    def test_root(self):
        # expect to get a list of files (a string with no Error keyword)
        result = get_files_info(self.dir_calculator, ".")
        print(result)  # Print the result
        self.assertNotIn("Error", result, "Expected no error in the result")

    def test_pkg(self):
        # expect to get a list of files (a string with no Error keyword)
        result = get_files_info(self.dir_calculator, "pkg")
        print(result)  # Print the result
        self.assertNotIn("Error", result, "Expected no error in the result")

    def test_bin(self):
        # Expects a str with the Keyword Error: at the front
        result = get_files_info(self.dir_calculator, "/bin")
        print(result)  # Print the result
        self.assertTrue(
            result.startswith("Error:"), "Expected result to start with 'Error:'"
        )

    def test_outside(self):
        # Expects a str with the Keyword Error: at the front
        result = get_files_info(self.dir_calculator, "../")
        print(result)  # Print the result
        self.assertTrue(
            result.startswith("Error:"), "Expected result to start with 'Error:'"
        )


if __name__ == "__main__":
    unittest.main()
