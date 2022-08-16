# -*- coding: utf-8 -*-
# cython: language_level=3
from libc.stdlib cimport malloc, free

cdef extern from "_jenks.c":
    void *JenksBreakValues(double *values, unsigned int nb_class,
                           unsigned int length_array, double *breaks)

cpdef _jenks_breaks(values, nb_class):
    cdef:
        list breaks = []
        unsigned int _nb_class = <unsigned int>int(nb_class)
        unsigned int _n_breaks = <unsigned int>_nb_class + 1
        unsigned int len_values = <unsigned int>len(values)
        unsigned int i = 0
        double *_values = <double *>malloc(len_values * sizeof(double))
        double *_breaks = <double *>malloc(_n_breaks * sizeof(double))

    for i in range(len_values):
        _values[i] = <double>values[i]

    JenksBreakValues(_values, _nb_class, len_values, _breaks)

    for i in range(<unsigned int>_n_breaks):
        breaks.append(_breaks[i])

    free(_values)
    free(_breaks)

    return breaks