#include <stdlib.h>
#include <float.h>
#include <sys/types.h>

int
compare_doubles (const void *a, const void *b)
{
  return (*(double *)a > *(double *)b) - (*(double *)a < *(double *)b);
}


static void
JenksBreakValues(double *values, unsigned int nb_class,
                 unsigned int length_array, double *breaks)
{
    int lower_class_limit, i4, k;
    unsigned int i=0, j=0, l=0, m=0;
    double variance, val, sum, sum_squares, w, temp_val;
    int **lower_class_limits = (int **)malloc((length_array + 1) * sizeof(int*)),
        *row_int = NULL;
    double **variance_combinations = (double **)malloc((length_array + 1) * sizeof(double*)),
        *row_double = NULL;

    // Sort the target array
    qsort(values, length_array, sizeof(double), compare_doubles);

    // Initialise the lower_class_limits and variance_combinations arrays
    for (i = 0; i < length_array + 1; i++) {
        row_int = (int *)malloc((nb_class + 1) * sizeof(int));
        memset(row_int, 0, (nb_class + 1) * sizeof(int));
        lower_class_limits[i] = row_int;
	}

    for (i = 0; i < length_array + 1; i++) {
        row_double = (double *)malloc((nb_class + 1) * sizeof(double));
        memset(row_double, 0.0, (nb_class + 1) * sizeof(double));
        variance_combinations[i] = row_double;
	}

    for (i = 1; i < nb_class + 1; i++) {
        lower_class_limits[0][i] = 1;
        lower_class_limits[1][i] = 1;
        for (j = 2; j < length_array + 1; j++) { variance_combinations[j][i] = DBL_MAX; }
    }

    variance = 0;
    for (l = 2; l < length_array + 1; l++) {
        sum = sum_squares = w = 0.0;
        for (m = 1; m < l + 1; m++) {
            lower_class_limit = l - m + 1;

            val = values[lower_class_limit - 1];

            w += 1.0;
            sum += val;
            sum_squares += val * val;
            variance = sum_squares - (sum * sum) / w;
            i4 = lower_class_limit - 1;

            if(i4 != 0) {
                for (j = 2; j < nb_class + 1; j++) {
                    temp_val = (variance + variance_combinations[i4][j - 1]);
                    if (fabs(variance_combinations[l][j] - temp_val) < DBL_EPSILON || variance_combinations[l][j] > temp_val) {
                        lower_class_limits[l][j] = lower_class_limit;
                        variance_combinations[l][j] = temp_val;
                    }
                }
            }
        }
        lower_class_limits[l][1] = 1;
        variance_combinations[l][1] = variance;
    }

    // Prepare the class limits
    k = length_array;
    // First value is the minimum of the target array
    breaks[0] = values[0];
    // Last value is the maximum of the target array
    breaks[nb_class] = values[(int)length_array - 1];

    for (j = nb_class; j > 1; j--) {
        breaks[j - 1] = values[lower_class_limits[k][j] - 2];
        k = lower_class_limits[k][j] - 1;
    }

    // Free lower_class_limits and variance_combinations arrays
    for (i = 0; i < length_array + 1; i++) {
        free(lower_class_limits[i]);
        free(variance_combinations[i]);
    }
    free(lower_class_limits);
    free(variance_combinations);
}
