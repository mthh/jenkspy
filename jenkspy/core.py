# -*- coding: utf-8 -*-
from collections import Iterable
from . import jenks


def jenks_breaks(values, nb_class):
    if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
        raise ValueError("A sequence of numbers is expected.")
    if nb_class >= len(values) or nb_class < 2:
        raise ValueError("Number of class have to be greater than 2 and "
                         "smaller than the number of values to use.")
    return jenks._jenks_breaks(values, nb_class)
