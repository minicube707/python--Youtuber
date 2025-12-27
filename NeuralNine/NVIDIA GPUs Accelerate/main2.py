import torch
import time

matrix_size =  5000

cpu_tensor1 =  torch.randn(matrix_size, matrix_size)
cpu_tensor2 =  torch.randn(matrix_size, matrix_size)

print("Checking GPU")
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.version.cuda)

if torch.cuda.is_available():
    gpu_tensor1 = cpu_tensor1.to('cuda')
    gpu_tensor2 = cpu_tensor2.to('cuda')

else:
    print("CUDA is not available. Make sure you have a GPU.")

start_time = time.time()
cpu_result = torch.matmul(cpu_tensor1, cpu_tensor2)
cpu_result = torch.matmul(cpu_result, cpu_tensor2)
cpu_result = torch.matmul(cpu_result, cpu_tensor2)
cpu_time = time.time() - start_time
print(f"Time taken on CPU: {cpu_time:.4f} seconds")

if torch.cuda.is_available():
    torch.cuda.synchronize()
    start_time = time.time()
    gpu_result = torch.matmul(gpu_tensor1, gpu_tensor2)
    gpu_result = torch.matmul(gpu_result, gpu_tensor2)
    gpu_result = torch.matmul(gpu_result, gpu_tensor2)
    torch.cuda.synchronize()
    gpu_time = time.time() - start_time
    print(f"Time taken on GPU: {gpu_time:.4f} seconds")

else:
    print("CUDA is not available, skipping GPU timing.")

