# -*- coding: utf-8 -*-
import unittest
import json
from jenkspy import jenks_breaks

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
        res = jenks_breaks(self.data1, 5)
        self.assertEqual(len(self.res1), len(res))
        for break_values in zip(res, self.res1):
            self.assertAlmostEqual(break_values[0], break_values[1], places=6)
        if np:
            data_np = np.array(self.data1)
            res_np = jenks_breaks(data_np, 5)
            self.assertEqual(res_np, res)

    def test_errors(self):
        with self.assertRaises(ValueError):
            jenks_breaks([1,2,3,4], 32)
        with self.assertRaises(ValueError):
            jenks_breaks("a sequence of characters", 4)
        with self.assertRaises(ValueError):
            jenks_breaks(self.data2, -5)

    def test_integers(self):
        res = jenks_breaks(self.data2, 4)
        for break_values in zip(res, self.res2):
            self.assertAlmostEqual(break_values[0], break_values[1], places=1)

if __name__ == "__main__":
    unittest.main()
