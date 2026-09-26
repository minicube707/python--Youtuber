import torch
import numpy as np


# ============================================================
# GPU / CUDA CHECK
# ============================================================

# Check whether CUDA (NVIDIA GPU support) is available.
# PyTorch can use the GPU to accelerate tensor computations.
if torch.cuda.is_available():
    # Display the number of available CUDA devices.
    print(torch.cuda.device_count())

    # Display the name of the current/default GPU.
    print(torch.cuda.get_device_name())

    # Display information about GPU device 0.
    print(torch.cuda.device(0))

else:
    print("No GPU available")


# ============================================================
# TENSORS
# ============================================================

# NumPy array
# NumPy is mainly used for numerical computing on the CPU.
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(f"{arr=}\n")


# Create a PyTorch tensor from a Python list.
# A tensor is the main data structure used by PyTorch.
tensor = torch.Tensor([[1, 2, 3], [4, 5, 6]])
print(f"{tensor=}\n")


# Element-wise multiplication:
# Each element of the array/tensor is multiplied by 5.
arr *= 5
print(f"{arr=}\n")
tensor *= 5
print(f"{tensor=}\n")


# Sum all elements.
# Both NumPy arrays and PyTorch tensors provide a .sum() operation.
print(f"{arr.sum()=}\n")
print(f"{tensor.sum()=}\n")


# ============================================================
# CONVERTING BETWEEN NUMPY AND PYTORCH
# ============================================================

# Convert a NumPy array into a PyTorch tensor.
#
# IMPORTANT:
# torch.from_numpy() creates a tensor that shares the same
# underlying memory with the NumPy array.
# This means that modifying one can affect the other.
tensor = torch.from_numpy(arr)
print(f"{tensor=}\n")


# Create an array/tensor filled with ones.
#
# NumPy version:
# np.ones((2, 4)) creates a 2x4 NumPy array.
print(f"{np.ones((2, 4))}\n")

# PyTorch version:
# torch.ones((2, 4)) creates a 2x4 PyTorch tensor.
print(f"{torch.ones((2, 4))}\n")


# ============================================================
# RANDOM VALUES
# ============================================================

# Generate a 2x4 NumPy array containing random values
# sampled from a uniform distribution between 0 and 1.
print(f"{np.random.random((2, 4))}\n")

# PyTorch equivalent:
# torch.rand() generates random values between 0 and 1.
print(f"{torch.rand((2, 4))}\n")


# ============================================================
# TENSOR / ARRAY PROPERTIES
# ============================================================

# Shape = dimensions of the array/tensor.
# Here, (2, 3) means 2 rows and 3 columns.
print(f"{arr.shape=}")

# dtype = data type of the values.
# For example: int64, float32, etc.
print(f"{arr.dtype=}")

# NumPy arrays do not have a .device attribute.
# They normally live in CPU memory.
#
# NOTE:
# This line will raise an AttributeError if uncommented.
# print(f"{arr.device=}")


# PyTorch tensor properties
print(f"{tensor.shape=}")

# dtype tells us the type used to store the tensor values.
print(f"{tensor.dtype=}")

# device tells us where the tensor is stored:
# - "cpu"  -> system RAM
# - "cuda" -> NVIDIA GPU memory
print(f"{tensor.device=}")


# ============================================================
# MOVING TENSORS TO THE GPU
# ============================================================

# NumPy arrays cannot directly be moved to the GPU.
# NumPy operations are normally performed on the CPU.
#
# arr.to_device('cuda')


# Move the PyTorch tensor to the GPU.
#
# This requires:
# 1. A CUDA-compatible NVIDIA GPU
# 2. A PyTorch installation with CUDA support
#
# tensor = tensor.to('cuda')


# Once the tensor is on the GPU, operations such as sum()
# will also be performed on the GPU.
#
# tensor.sum()


# ============================================================
# MOVING DATA BACK TO THE CPU
# ============================================================

# A CUDA tensor must be moved back to the CPU before
# converting it to a NumPy array.
#
# .cpu()    -> move tensor from GPU to CPU
# .numpy()  -> convert PyTorch tensor to NumPy array
#
# tensor.cpu().numpy()
