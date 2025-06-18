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
        self.assertFalse(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )

    def test_pkg(self):
        # expect to get a list of files (a string with no Error keyword)
        result = get_files_info(self.dir_calculator, "pkg")
        self.assertFalse(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )

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
        real_file = Path(self.dir_calculator) / "lorem.txt"

        real_size = os.path.getsize(real_file)

        self.assertFalse(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )
        self.assertLess(len(result), real_size)

    def test_content_main(self):
        # Expects a str with the Keyword Error: at the front
        result = get_file_contents(self.dir_calculator, "main.py")
        print(result)
        self.assertFalse(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )

    def test_content_calculator(self):
        # Expects a str with the Keyword Error: at the front
        result = get_file_contents(self.dir_calculator, "pkg/calculator.py")
        print(result)
        self.assertFalse(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )

    def test_content_cat_error(self):
        # Expects a str with the Keyword Error: at the front
        result = get_file_contents(self.dir_calculator, "/bin/cat")
        print(result)
        self.assertTrue(
            result.startswith("Error:"),
            "Expected the result not to start with 'Error:'",
        )


if __name__ == "__main__":
    unittest.main()
