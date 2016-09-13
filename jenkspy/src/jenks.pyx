# -*- coding: utf-8 -*-
from collections import Iterable
from libc.stdlib cimport malloc, free

cdef extern from "_jenks.c":
    void *JenksBreakValues(double *values, unsigned int nb_class,
                           unsigned int length_array, double *breaks)

cpdef _jenks_breaks(values, nb_class):
    cdef:
        list breaks = []
        unsigned int _n_breaks = int(nb_class) + 1
        unsigned int len_values = len(values), i = 0
        double *_values = <double *>malloc(<unsigned int>len_values * sizeof(double))
        double *_breaks = <double *>malloc(<unsigned int>_n_breaks * sizeof(double))

    for i in range(len_values):
        _values[i] = <double>values[i]

    JenksBreakValues(_values, <unsigned int>_n_breaks - 1, len_values, _breaks)

    for i in range(<unsigned int>_n_breaks):
        breaks.append(_breaks[i])

    free(_values)
    free(_breaks)

    return breaks