# -*- coding: utf-8 -*-
import unittest
import json
from jenkspy import jenks_breaks
from array import array
try:
	import numpy as np
except ImportError:
	np = None

class JenksClassTestCase(unittest.TestCase):
    def setUp(self):
        with open('tests/test.json', 'r') as f:
            self.data1 = json.loads(f.read())
        self.data2 = [132, 915, 312, 1424, 1240, 1370, 113, 1028, 1078, 416,
                      963, 359, 1422, 658, 73, 1326, 245, 848, 683, 255, 1223,
                      253, 654, 736, 1079, 39, 583, 1367, 1237, 327, 1083, 328,
                      951, 678, 927, 301, 96, 297, 179, 230, 767, 1248, 1, 37,
                      1352, 1009, 663, 1283, 679, 230]

        self.res1 = (0.002810962, 2.0935481, 4.2054954, 6.1781483, 8.0917587, 9.997983)
        self.res2 = (1.0, 416.0, 767.0, 1083.0, 1424.0)

    def test_json_ref(self):
        # Test it against break values computed using another library
        # implementing jenks natural breaks:
        res = jenks_breaks(self.data1, 5)
        self.assertEqual(len(self.res1), len(res))
        for break_values in zip(res, self.res1):
            self.assertAlmostEqual(break_values[0], break_values[1], places=6)

        # Test the result is the same using a python array as input:
        res_py_array = jenks_breaks(array('d', self.data1), 5)
        self.assertEqual(len(self.res1), len(res_py_array))
        for break_values in zip(res_py_array, self.res1):
            self.assertAlmostEqual(break_values[0], break_values[1], places=6)

        # Test the result is the same using a numpy array as input:
        if np:
            data_np = np.array(self.data1)
            res_np = jenks_breaks(data_np, 5)
            self.assertEqual(res_np, res)

    def test_errors(self):
        # Using wrong 'nb_class' argument:
        with self.assertRaises(ValueError):
            jenks_breaks([1,2,3,4], 32)
        with self.assertRaises(ValueError):
            jenks_breaks(self.data2, -5)
        # Using a wrong 'values' argument:
        with self.assertRaises(TypeError):
            jenks_breaks("a sequence of characters", 4)
        with self.assertRaises(TypeError):
            jenks_breaks(['a', 'b', 'c', 'd'], 3)
        # Using a serie of values containing NaN or Inf values,
        # the serie will now be too short for 4 class:
            with self.assertRaises(ValueError):
                self.assertWarns(
                    UserWarning,
                    jenks_breaks,
                    [1, 2, float('Inf'), float('NaN')], 4)
        # Same with numpy array:
        if np:
            with self.assertRaises(ValueError):
                self.assertWarns(
                    UserWarning,
                    jenks_breaks,
                    np.array([1, 2, float('Inf'), float('NaN')]), 4)

    def test_warnings(self):
        self.assertWarns(
            UserWarning,
            jenks_breaks,
            [1, 2, 3, 4, 5, float('Inf'), float('NaN'), 12], 3)

    def test_integers(self):
        # The algorythm works using a list/an array of integer:
        res = jenks_breaks(self.data2, 4)
        for break_values in zip(res, self.res2):
            self.assertAlmostEqual(break_values[0], break_values[1], places=1)

    def test_nb_class(self):
        # Using wrong 'nb_class' argument:
        with self.assertRaises(TypeError):
            jenks_breaks([1,2,3,4], [2])
        with self.assertRaises(TypeError):
            jenks_breaks([1,2,3,4], "a")

        # Using an integer as a float value for nb_class (allowed):
        res1 = jenks_breaks(self.data2, 4)
        res2 = jenks_breaks(self.data2, 4.0)
        for break_values in zip(res1, res2):
            self.assertAlmostEqual(break_values[0], break_values[1], places=1)

        # Really trying to use a float value as 'nb_class' (not allowed):
        with self.assertRaises(TypeError):
            jenks_breaks(self.data2, 4.7)


if __name__ == "__main__":
    unittest.main()
