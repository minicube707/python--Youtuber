import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import time

N_values = []
np_time = []
cp_time = []

# Perform warm up calculation to get CuPy running (show difference with and without)
# Initilisation takes time (first time only)
def warm_up_cupy():
    A = cp.ones((10, 10))
    B = cp.ones((10, 10)) 
    _ = cp.dot(A, B)

warm_up_cupy()

for N in range (1000, 13000, 1000):
    A_np = np.random.randn(N, N)
    B_np = np.random.randn(N, N)

    start_time = time.time()
    C_np = np.dot(A_np, B_np)
    D_np = np.dot(C_np, A_np)
    E_np = np.dot(D_np, B_np)
    numpy_time = time.time() - start_time

    start_time = time.time()
    A_cp = cp.asarray(A_np)
    B_cp = cp.asarray(B_np)
    C_cp = np.dot(A_cp, B_cp)
    D_cp = np.dot(C_cp, A_cp)
    E_cp = np.dot(D_cp, B_cp)
    E_cp_cpu = cp.asnumpy(E_cp)
    cupy_time = time.time() - start_time

    N_values.append(N)
    np_time.append(numpy_time)
    cp_time.append(cupy_time)

plt.plot(N_values, np_time, label='Numpy Time')
plt.plot(N_values, cp_time, label='CuPy Time')
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (s)')
plt.title("NumPy Vs CuPy Performance (With Conversion & More Calculatoins)")
plt.grid(True)
plt.legend()
plt.savefig('comparaison3.png')
plt.show()