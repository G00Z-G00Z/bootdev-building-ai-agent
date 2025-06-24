# tests.py

import os
from pathlib import Path
import unittest

from functions.get_files_info import (
    write_file,
)


class TestGetFilesInfo(unittest.TestCase):

    dir_calculator: str

    def setUp(self):
        wd = os.getcwd()
        self.dir_calculator = str(Path(wd) / "calculator")

    def test_write_files(self):
        result = write_file(
            self.dir_calculator, "lorem.txt", "wait, this isn't lorem ipsum"
        )
        print(result)
        self.assertIn(
            "Successfully wrote to", result, "Did not successfully write to the file"
        )

        result = write_file(
            self.dir_calculator, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(result)
        self.assertIn(
            "Successfully wrote to", result, "Did not successfully write to the file"
        )
        result = write_file(
            self.dir_calculator, "/tmp/temp.txt", "this should not be allowed"
        )
        print(result)
        self.assertNotIn(
            "Successfully wrote to", result, "Did not successfully write to the file"
        )
        self.assertTrue(result.startswith("Error: "), "Expected to get an error")


if __name__ == "__main__":
    unittest.main()
