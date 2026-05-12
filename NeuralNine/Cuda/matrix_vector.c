#include <stdio.h>
#include <stdlib.h>

/*
 * Computes the product of a square matrix A and a vector v1.
 *
 * Parameters:
 *   A            -> Pointer to the matrix stored in row-major order
 *   v1           -> Input vector
 *   v2           -> Output vector containing the result
 *   matrix_size  -> Number of rows/columns in the square matrix
 */
void matrix_vector_product(float *A, float *v1, float *v2, int matrix_size)
{
    // Iterate through each row of the matrix
    for (int i = 0; i < matrix_size; i++)
    {
        float sum = 0.0f;

        // Compute the dot product between row i and vector v1
        for (int j = 0; j < matrix_size; j++)
        {
            sum += A[i * matrix_size + j] * v1[j];
        }

        // Store the result in the output vector
        v2[i] = sum;
    }
}

int main(int argc, char **argv)
{
    // Pointers for the matrix and vectors
    float *A, *v1, *v2;

    // Size of the square matrix
    int matrix_size = 40000;

    // Allocate memory for the matrix and vectors
    A = (float *) malloc(matrix_size * matrix_size * sizeof(float));
    v1 = (float *) malloc(matrix_size * sizeof(float));
    v2 = (float *) malloc(matrix_size * sizeof(float));

    // Initialize the matrix with increasing values
    for (int i = 0; i < matrix_size; i++)
    {
        for (int j = 0; j < matrix_size; j++)
            A[i * matrix_size + j] = (float) i * matrix_size + j;
    }

    // Initialize the input vector
    for (int i = 0; i < matrix_size; i++)
        v1[i] = (float) i;

    // Perform matrix-vector multiplication
    matrix_vector_product(A, v1, v2, matrix_size);

    // Print the resulting vector
    for (int i = 0; i < matrix_size; i++)
        printf("%.2f\n", v2[i]);

    // Free allocated memory
    free(A);
    free(v1);
    free(v2);

    return 0;
}