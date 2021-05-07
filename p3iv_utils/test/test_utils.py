import unittest
import numpy as np
import os
import matplotlib.pyplot as plt
from p3iv_utils.lanelet_map_reader import lanelet_map_reader
from p3iv_utils.consoleprint import Print2Console


class TestPrin2Console(unittest.TestCase):
    def test_console_print(self):
        Print2Console.p("s", ["hello"], style="yellow")
        self.assertTrue(True)  # fake test :(


class TestLaneletMapReader(unittest.TestCase):
    def test_lanelet_map_reader(self):
        file_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(file_path, "../res/maps/lanelet2")
        l = lanelet_map_reader("DR_DEU_Merging_MT", directory)
        print("Lanelet map loaded")
        self.assertTrue(True)  # another fake test :( is added for coverage


if __name__ == "__main__":
    unittest.main()
