import numpy as np
from numba import cuda, float32, njit
import time

N = 50000000

a =  np.random.randn(N).astype(np.float32)
b =  np.random.randn(N).astype(np.float32)
c =  np.zeros_like(a)

# Pure Python
def add_arrays_python(a, b, c):
    for i in range(N):
        c[i] = a[i] + b [i]

# Numba njit
@njit
def add_arrays_njit(a, b, c):
    for i in range(N):
        c[i] = a[i] + b [i]

# CUDA kernel
@cuda.jit
def add_arrays_cuda(a, b, c):
    idx = cuda.grid(1)
    if (idx < c.size):
        c[idx] = a[idx] + b[idx]


# Pure Python timing
start_time = time.time()
add_arrays_python(a, b, c)
python_time = time.time() - start_time
print(f"Pure Python time: {python_time:.4f} seconds")

c[:] = 0

# Numba njit timing
start_time = time.time()
add_arrays_njit(a, b, c)
njit_python_time = time.time() - start_time
print(f"njit Python time: {njit_python_time:.4f} seconds")

c[:] = 0

# CUDA
a_device = cuda.to_device(a)
b_device = cuda.to_device(b)
c_device = cuda.device_array_like(c)

threads_per_block = 256
blocks_per_grid = (N + threads_per_block - 1) // threads_per_block

# Warm-up
add_arrays_cuda[blocks_per_grid, threads_per_block](a_device, b_device, c_device)
cuda.synchronize()

# Timing CUDA
start_time = time.time()
add_arrays_cuda[blocks_per_grid, threads_per_block](a_device, b_device, c_device)
cuda.synchronize()
cuda_time = time.time() - start_time
print(f"CUDA time (excluding data transfer): {cuda_time:.4f} seconds")

c_device.copy_to_host(c)

assert np.allclose(c, a + b), "Verification failed: The results are incorect."

speedup = python_time / cuda_time if cuda_time > 0 else float('inf')
speedup_njit = njit_python_time / cuda_time if cuda_time > 0 else float('inf')
print(f"Speedup: {speedup:.2f}x faster than Pure Python with CUDA")
print(f"Speedup: {speedup_njit:.2f}x faster than njit with CUDA")