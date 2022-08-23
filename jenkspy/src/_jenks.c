#include <stdlib.h>
#include <float.h>
#include <sys/types.h>

// Macro to access the elements of our matrices
#define IX(i,j) (i)*(width)+(j)

// Compute FisherJenks matrices.
// Compared to fish.f code, some arithmetic might seem
// a little different but this is because we use C arrays whose values start at 0
// and not Fortran arrays (and also because most other implementations
// at the time of writing (in Python, JS, etc.)
// don't take care to simplify these calculations).
// See also the comments below about this.
// ----------------------------------------------------------------------------
// Parameters:
//   variance_combinations: array of length 'length_array' * 'n_classes' (modified)
//   lower_class_limits: array of length 'length_array' * 'n_classes' (modified)
//   values: sorted array of data values (unmodified)
//   n_classes: number of classes
//   length_array: length of the 'values' array
static void
JenksMatrices(double *variance_combinations, int *lower_class_limits, double *values, unsigned int n_classes, unsigned int length_array) {
    int lower_class_limit, i4;
    unsigned int i, j, l, m;
    double variance, val, sum, sum_squares, w, temp_val;
    // The width of the two matrices - this value is used in IX macro
    unsigned int width = n_classes;

    // Initialise the matrices with the expected value, as per fish.f code
    for (j = 0; j < n_classes; j++) {
        lower_class_limits[IX(0, j)] = 1;
        for (i = 0; i < length_array; i++) {
            variance_combinations[IX(i, j)] = DBL_MAX;
        }
    }

    variance = 0;
    for (l = 0; l < length_array; l++) {
        sum = sum_squares = w = 0.0;

        for (m = 0; m <= l; m++) {

            lower_class_limit = l - m;
            val = values[lower_class_limit];

            w += 1.0;
            sum += val;
            sum_squares += val * val;
            variance = sum_squares - (sum * sum) / w;
            i4 = lower_class_limit - 1;

            if(i4 > -1) {
                for (j = 1; j < n_classes; j++) {
                    temp_val = (variance + variance_combinations[IX(i4, j - 1)]);
                    if (variance_combinations[IX(l, j)] >= temp_val) {
                        // We still add '1' because fish.f code uses 1-based indexing
                        // and we want to obtain the exact same result for later testing
                        // (we take this into account when actually building the breaks array in Python code -
                        //  also note that changing this, ie not adding 1 here, would also require to initialise the
                        //  array at 0 and not 1, line 32 and 68 of this file):
                        lower_class_limits[IX(l, j)] = lower_class_limit + 1;
                        variance_combinations[IX(l, j)] = temp_val;
                    }
                }
            }
        }
        lower_class_limits[IX(l, 0)] = 1;
        variance_combinations[IX(l, 0)] = variance;
    }
}

// Macro to access the elements of our matrices
// using the same arithmetic than fish.f
// (with fortran array that starts at 1)
#define IXF(i,j) ((i)-1)*(width)+((j)-1)
#define I(i) ((i)-1)

// Compute FisherJenks matrices.
// It use the same arithmetic as in fish.f, so we can verify that the results are the same
// (this function is *not* used when calling 'jenks_breaks' but only when calling
// 'jenks_matrices' with the arguments "testing_algo" set to True).
// ----------------------------------------------------------------------------
// Parameters:
//   variance_combinations: array of length 'length_array' * 'n_classes' (modified)
//   lower_class_limits: array of length 'length_array' * 'n_classes' (modified)
//   values: sorted array of data values (unmodified)
//   n_classes: number of classes
//   length_array: length of the 'values' array
static void
JenksMatricesTest(double *variance_combinations, int *lower_class_limits, double *values, unsigned int n_classes, unsigned int length_array) {
    int lower_class_limit, i4;
    unsigned int i, j, l, m;
    double variance, val, sum, sum_squares, w;
    // The width of the two matrices - this value is used in IXF macro
    unsigned int width = n_classes;

    // Initialise the matrices with the expected value, as per fish.f code
    for (j = 1; j <= n_classes; j++) {
        lower_class_limits[IXF(1, j)] = 1;
        variance_combinations[IXF(1, j)] = 0.0;
        // ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        // We do this to exactly mimic the original code (as this is our testing function)
        // but this is useless as we will overwrite the values in the following loop:
        for (i = 1; i <= length_array; i++) {
            variance_combinations[IXF(i, j)] = DBL_MAX;
        }
    }

    variance = 0;
    for (l = 1; l <= length_array; l++) {
        sum = sum_squares = w = 0.0;

        for (m = 1; m <= l; m++) {

            lower_class_limit = l - m + 1;
            val = values[I(lower_class_limit)];

            w = (double) m;
            sum += val;
            sum_squares += val * val;
            variance = sum_squares - (sum * sum) / w;
            i4 = lower_class_limit - 1;

            if(i4 != 0) {
                for (j = 2; j <= n_classes; j++) {
                    if (variance_combinations[IXF(l, j)] >= (variance + variance_combinations[IXF(i4, j - 1)])) {
                        lower_class_limits[IXF(l, j)] = lower_class_limit;
                        variance_combinations[IXF(l, j)] = (variance + variance_combinations[IXF(i4, j - 1)]);
                    }
                }
            }
        }
        lower_class_limits[IXF(l, 1)] = 1;
        variance_combinations[IXF(l, 1)] = variance;
    }
}
