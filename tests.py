# tests.py

import os
from pathlib import Path
import unittest

from functions.get_files_info import (
    run_python_file,
)


class TestGetFilesInfo(unittest.TestCase):

    dir_calculator: str

    def setUp(self):
        wd = os.getcwd()
        self.dir_calculator = str(Path(wd) / "calculator")

    def test_run_python(self):

        result = run_python_file(self.dir_calculator, "main.py")
        print(result)
        self.assertFalse(result.startswith("Error: "), "Expected to get an error")

        result = run_python_file(self.dir_calculator, "tests.py")
        print(result)
        self.assertFalse(result.startswith("Error: "), "Expected to get an error")

        result = run_python_file(self.dir_calculator, "../main.py")
        print(result)
        self.assertTrue(result.startswith("Error: "), "Expected to get an error")

        result = run_python_file(self.dir_calculator, "nonexistent.py")
        print(result)
        self.assertTrue(result.startswith("Error: "), "Expected to get an error")


if __name__ == "__main__":
    unittest.main()
