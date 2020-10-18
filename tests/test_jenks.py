# -*- coding: utf-8 -*-
import unittest
import json
from jenkspy import jenks_breaks
from jenkspy import JenksNaturalBreaks
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
        self.res3 = [1.0, 416.0, 767.0, 1083.0, 1424.0]
        self.res4 = [416.0, 767.0, 1083.0]
        if np:
            self.res5 = np.array([0, 2, 0, 3, 3, 3, 0, 2, 2, 0, 2, 0, 3, 1, 0, 3, 0, 2, 1, 0, 3, 0, 1, 1, 2, 0, 1, 3, 3, 0, 2, 0, 2, 1, 2, 0, 0, 0, 0, 0, 1, 3, 0, 0, 3, 2, 1, 3, 1, 0])
            self.res6 = [np.array([132, 312, 113, 416, 359, 73, 245, 255, 253, 39, 327, 328, 301, 96, 297, 179, 230, 1, 37, 230]), np.array([658, 683, 654, 736, 583, 678, 767, 663, 679]), np.array([915, 1028, 1078, 963, 848, 1079, 1083, 951, 927, 1009]), np.array([1424, 1240, 1370, 1422, 1326, 1223, 1367, 1237, 1248, 1352, 1283])]
            self.res7 = np.array([0,1])
            self.res8 = [np.array([150]), np.array([]), np.array([]), np.array([])]
            self.res9 = [np.array([150]), np.array([700]), np.array([]), np.array([])]
        
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

    def test_calling_JenksNaturalBreaks_class(self):
        # test calling JenksNaturalBreaks:
        jnb = JenksNaturalBreaks()
        self.assertEqual(type(jnb).__name__,'JenksNaturalBreaks')

        jnb = JenksNaturalBreaks(nb_class=4)
        self.assertEqual(jnb.nb_class,4)
    
    def test_JenksNaturalBreaks_fit(self):
        jnb = JenksNaturalBreaks(nb_class=4)
        jnb.fit(self.data2)
        self.assertEqual(jnb.breaks_,self.res3)
        self.assertEqual(jnb.inner_breaks_,self.res4)
        if np:
            self.assertEqual((jnb.labels_==self.res5).all(),True)
            self.assertEqual(type(jnb.labels_).__name__,type(np.array([self.res5])).__name__)
            for group_fit, group_true in zip(jnb.groups_, self.res6):
                self.assertEqual((group_fit==group_true).all(),True)

    def test_test_JenksNaturalBreaks_predict(self):
        if np:
            # predict before fit (not allowed)
            jnb = JenksNaturalBreaks(nb_class=4)
            with self.assertRaises(AttributeError):
                jnb.predict(150)
        
            # predict single value
            jnb.fit(self.data2)
            self.assertEqual(jnb.predict(150),0)

            # predict iterable return numpy array
            predicted = jnb.predict([150,700])
            for val_predict, val_true in zip(predicted, self.res7):
                self.assertEqual(val_predict,val_true)
                self.assertEqual(type(val_predict).__name__,type(val_true).__name__)

    def test_grouping(self):
        if np:
            # grouping before fit (not allowed)
            jnb = JenksNaturalBreaks(nb_class=4)
            with self.assertRaises(AttributeError):
                jnb.group(150)

            # grouping single value, list, numpy array
            jnb.fit(self.data2)
            for group_fit, group_true in zip(jnb.group(150), self.res8):
                self.assertEqual((group_fit==group_true).all(),True)
            for group_fit, group_true in zip(jnb.group([150,700]), self.res9):
                self.assertEqual((group_fit==group_true).all(),True)
            for group_fit, group_true in zip(jnb.group(np.array([150,700])), self.res9):
                self.assertEqual((group_fit==group_true).all(),True)

if __name__ == "__main__":
    unittest.main()
