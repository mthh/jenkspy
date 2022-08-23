# -*- coding: utf-8 -*-
# cython: language_level=3
from libc.stdlib cimport malloc, free
import numpy as np

cdef extern from "_jenks.c":
    void *JenksMatrices(double *variance_combinations, int *lower_class_limits, double *values, unsigned int n_classes, unsigned int length_array)
    void *JenksMatricesTest(double *variance_combinations, int *lower_class_limits, double *values, unsigned int n_classes, unsigned int length_array)


cpdef list _jenks_breaks(values, n_classes):
    cdef:
        list breaks = []
        unsigned int _n_classes = <unsigned int>int(n_classes) # How many classes (clusters)
        unsigned int _n_breaks = <unsigned int>_n_classes + 1 # How many class boundaries
        unsigned int len_values = <unsigned int>len(values) # How many values to classify
        unsigned int i
        int *_lower_class_limits = <int *> malloc((len_values * _n_classes) * sizeof(int))
        double *_variance_combinations = <double *> malloc((len_values * _n_classes) * sizeof(double))
        unsigned int m, k, jj # Indexes for fetching break values from _lower_class_limits matrix
        sorted_values = np.sort(values) # Sort the values to classify
        double[:] _sorted_values = sorted_values.astype(np.float64) # Convert to double array

    # Fill the lower_class_limits and variance_combinations matrices
    JenksMatrices(_variance_combinations, _lower_class_limits, &_sorted_values[0], _n_classes, len_values)

    # Fill the breaks array with minimum value of the target array
    for i in range(_n_breaks):
        breaks.append(sorted_values[0])

    # Last break value is the maximum of the array
    breaks[_n_classes] = sorted_values[-1]

    # Read the class limits from the lower_class_limits matrix
    m = len_values
    for j in range(1, _n_classes):
        jj = _n_classes - j + 1
        # Note that the indexes contained in the _lower_class_limits matrix are 1-based,
        # so we have to subtract 1 to get the correct index
        breaks[jj - 1] = sorted_values[_lower_class_limits[(m - 1) * _n_classes + (jj - 1)] - 2]
        m = _lower_class_limits[(m - 1) * _n_classes + (jj - 1)] - 1

    # Free memory we manually allocated
    free(<void *>_lower_class_limits)
    free(<void *>_variance_combinations)

    return breaks

cpdef dict _jenks_matrices(values, n_classes, testing_algo=False):
    cdef:
        unsigned int _n_classes = <unsigned int>int(n_classes) # How many classes (clusters)
        unsigned int len_values = <unsigned int>len(values) # How many values to classify
        unsigned int i
        int *_lower_class_limits = <int *> malloc((len_values * _n_classes) * sizeof(int))
        double *_variance_combinations = <double *> malloc((len_values * _n_classes) * sizeof(double))
        unsigned int m, k, jj # Indexes for fetching break values from _lower_class_limits matrix
        list lower_class_limits = []
        list variance_combinations = []
        sorted_values = np.sort(values) # Sort the values to classify
        double[:] _sorted_values = sorted_values.astype(np.float64) # Convert to double array

    # Fill the lower_class_limits and variance_combinations matrices
    if not testing_algo:
        JenksMatrices(_variance_combinations, _lower_class_limits, &_sorted_values[0], _n_classes, len_values)
    else:
        JenksMatricesTest(_variance_combinations, _lower_class_limits, &_sorted_values[0], _n_classes, len_values)

    # Reconstruct the lower class limits matrix and the variance combinations matrix
    # from the 1D arrays that we use in C code
    for i in range(len_values):
        lower_class_limits.append([])
        variance_combinations.append([])
        for j in range(_n_classes):
            lower_class_limits[i].append(_lower_class_limits[i * _n_classes + j])
            variance_combinations[i].append(_variance_combinations[i * _n_classes + j])

    # Free memory we manually allocated
    free(<void *>_lower_class_limits)
    free(<void *>_variance_combinations)

    return {
        "lower_class_limits": np.array(lower_class_limits),
        "variance_combinations": np.array(variance_combinations),
    }

