#include <stdio.h>

/*
 * CUDA kernel that computes the product of a square matrix A
 * and a vector v1.
 *
 * Each thread is associated with one matrix element position.
 * Only threads with col == 0 perform the computation for a row.
 *
 * Parameters:
 *   A            -> Input matrix stored in row-major order
 *   v1           -> Input vector
 *   v2           -> Output vector
 *   matrix_size  -> Number of rows/columns in the matrix
 */
__global__ void matrix_vector_product(float *A, float *v1, float *v2, int matrix_size)
{
   // Compute the global row index handled by the thread
   int row = blockIdx.x * blockDim.x + threadIdx.x;

   // Compute the global column index handled by the thread
   int col = blockIdx.y * blockDim.y + threadIdx.y;

   // Only one thread per row performs the computation
   if (col == 0 && row < matrix_size)
   {
        float sum = 0.0f;

        // Compute the dot product between row 'row' and vector v1
        for (int i = 0; i < matrix_size; i++)
        {
            sum += A[row * matrix_size + i] * v1[i];
        }

        // Store the result in the output vector
        v2[row] = sum;
   }
}

int main(int argc, char **argv)
{
    // Host and device pointers for the matrix and vectors
    float *A, *A_gpu;
    float *v1, *v1_gpu;
    float *v2, *v2_gpu;

    // Size of the square matrix
    int matrix_size = 40000;

    // Define CUDA block dimensions (32x32 threads per block)
    dim3 block_shape = dim3(32, 32);

    // Define CUDA grid dimensions
    dim3 grid_shape = dim3(
        max(1.0, ceil((float) matrix_size / (float) block_shape.x)),
        max(1.0, ceil((float) matrix_size / (float) block_shape.y))
    );

    // Allocate host memory
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

    // Allocate GPU memory
    cudaMalloc((void **) &A_gpu, matrix_size * matrix_size * sizeof(float));
    cudaMalloc((void **) &v1_gpu, matrix_size * sizeof(float));
    cudaMalloc((void **) &v2_gpu, matrix_size * sizeof(float));

    // Copy data from host memory to GPU memory
    cudaMemcpy(A_gpu, A,
               matrix_size * matrix_size * sizeof(float),
               cudaMemcpyHostToDevice);

    cudaMemcpy(v1_gpu, v1,
               matrix_size * sizeof(float),
               cudaMemcpyHostToDevice);

    // Launch the CUDA kernel
    matrix_vector_product<<<grid_shape, block_shape>>>(
        A_gpu, v1_gpu, v2_gpu, matrix_size
    );

    // Copy the result back from GPU to host memory
    cudaMemcpy(v2, v2_gpu,
               matrix_size * sizeof(float),
               cudaMemcpyDeviceToHost);

    // Print the resulting vector
    for (int i = 0; i < matrix_size; i++)
        printf("%.2f\n", v2[i]);

    // Free host memory
    free(A);
    free(v1);
    free(v2);

    // Free GPU memory
    cudaFree(A_gpu);
    cudaFree(v1_gpu);
    cudaFree(v2_gpu);

    return 0;
}