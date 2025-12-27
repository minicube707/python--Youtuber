#Code run under python 3.11

import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import time
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


batch_size = 64
learning_rate = 0.001
epochs = 1

class CNN(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307, ), (0.3081, ))])
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('.', train=True, download=True, transform=transform),
    batch_size=batch_size, shuffle=True
)

def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate (train_loader):
        data = data.to(device)
        target = target.to(device)

        optimizer.zero_grad()
        output =  model(data)
        loss = nn.CrossEntropyLoss()(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            print(f"Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)}] Loss: {loss.item():.6f}")

#CPU
cpu_device = torch.device("cpu")
model_cpu =  CNN().to(cpu_device)
optimizer_cpu = optim.Adam(model_cpu.parameters(), lr=learning_rate)

print("\nTraining on CPU...")
start_time = time.time()
for epoch in range(1, epochs + 1):
    train(model_cpu, cpu_device, train_loader, optimizer_cpu, epoch)
cpu_time = time.time() - start_time
print(f"Time taken on CPU {cpu_time:.2f} seconds")

#GPU
if torch.cuda.is_available():
    gpu_device = torch.device("cuda")
    model_gpu =  CNN().to(gpu_device)
    optimizer_gpu = optim.Adam(model_gpu.parameters(), lr=learning_rate)

    print("\nTraining on GPU...")
    torch.cuda.synchronize()
    start_time = time.time()
    for epoch in range(1, epochs + 1):
        train(model_gpu, gpu_device, train_loader, optimizer_gpu, epoch)
    torch.cuda.synchronize()
    gpu_time = time.time() - start_time
    print(f"Time taken on GPU {gpu_time:.2f} seconds")
else:
    print("CUDA is not available, skipping GPU timing.")