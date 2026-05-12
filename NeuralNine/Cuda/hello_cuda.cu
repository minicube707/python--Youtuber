#include <stdio.h>

// CUDA kernel executed on the GPU
__global__ void hello_cuda()
{
    // Print a simple message from each thread
    printf("Hello Cuda\n");

    // Display block and thread indices for each executing thread
    printf("Block Index X: %d, Block Index Y: %d, Thread Index X: %d, Thread Index Y: %d\n",
        blockIdx.x, blockIdx.y, threadIdx.x, threadIdx.y);
}

int main(int argc, char **argv)
{
    // Launch the kernel with:
    // - 2 blocks
    // - 2 threads per block
    hello_cuda<<<2, 2>>>();

    // Wait for the GPU to finish execution before exiting
    cudaDeviceSynchronize();

    return 0;
}