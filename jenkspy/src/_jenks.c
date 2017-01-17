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
    int i3, i4;
    unsigned int i=0, j=0, l=0, m=0, k = nb_class;
    double v, val, s1, s2, w;
    double *kclass = NULL;
    double **mat1 = (double **)malloc(length_array * sizeof(double*)),
        **mat2 = (double **)malloc(length_array * sizeof(double*)),
        *row = NULL;

    qsort(values, length_array, sizeof(double), compare_doubles);

    for (i = 0; i < length_array; i++) {
        row = (double *)malloc(k * sizeof(double));
        for (j = 0; j < k; j++) { row[j] = 1.0; }
        mat1[i] = row;
	}

    for (i = 0; i < length_array; i++) {
        row = (double *)malloc(k * sizeof(double));
        for (j = 0; j < k; j++) { row[j] = FLT_MAX; }
        mat2[i] = row;
	}

    v = 0;
    for (l = 2; l <= length_array; l++) {
        s1 = s2 = w = 0;
        for (m = 1; m <= l; m++) {
            i3 = l - m + 1;
            val = values[(i3-1)];
            s2 += val * val;
            s1 += val;
            w++;
            v = s2 - (s1 * s1) / w;
            i4 = i3 - 1;

            if(i4) {
                for (j = 2; j <= k; j++) {
                    if (mat2[l-1][j-1] >= (v + mat2[i4-1][j-2])) {
                        mat1[l-1][j-1] = i3;
                        mat2[l-1][j-1] = v + mat2[i4-1][j-2];
                        }
                }
            }
        }
        mat1[l-1][0] = 1;
        mat2[l-1][0] = v;
    }

    kclass = (double *)malloc(k * sizeof(double));
    k = length_array;
    for (j = nb_class; j > 1; j--) {
        kclass[j - 2] = k = (int)(mat1[k-1][j-1]) - 1;
    }
    breaks[0] = values[0];
    for (i = 1; i < nb_class; i++) {
        breaks[i] = values[(int)(kclass[i - 1]) - 1];
    }
    breaks[nb_class] = values[(int)length_array-1];

    for (i = 0; i < length_array; i++) {
        free(mat1[i]);
        free(mat2[i]);
    }
    free(mat1);
    free(mat2);
    free(kclass);
}
