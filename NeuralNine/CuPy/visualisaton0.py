import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import time

N_values = []
np_time = []
cp_time = []

for N in range (1000, 11000, 1000):
    A_np = np.random.randn(N, N)
    B_np = np.random.randn(N, N)

    A_cp = cp.asarray(A_np)
    B_cp = cp.asarray(B_np)

    start_time = time.time()
    C_np = np.dot(A_np, B_np)
    numpy_time = time.time() - start_time

    start_time = time.time()
    C_cp = np.dot(A_cp, B_cp)
    cupy_time = time.time() - start_time

    N_values.append(N)
    np_time.append(numpy_time)
    cp_time.append(cupy_time)

plt.plot(N_values, np_time, label='Numpy Time')
plt.plot(N_values, cp_time, label='CuPy Time')
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (s)')
plt.title("NumPy Vs CuPy Performance (No Warm-UP)")
plt.grid(True)
plt.legend()
plt.savefig('comparaison0.png')
plt.show()