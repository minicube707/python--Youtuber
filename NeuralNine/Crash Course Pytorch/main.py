import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. LOAD THE DATASET
# ============================================================

# Load the Breast Cancer Wisconsin dataset from scikit-learn.
#
# X contains the input features.
# y contains the binary target labels.
#
# The dataset contains:
# - 569 samples
# - 30 numerical features
# - 2 possible classes
X, y = load_breast_cancer(return_X_y=True)


# Split the data into training and testing sets.
#
# 80% of the data will be used for training.
# 20% will be used for evaluating the model.
#
# random_state can be specified to make the split reproducible.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)


# ============================================================
# 2. STANDARDIZE THE FEATURES
# ============================================================

# StandardScaler transforms each feature so that it has
# approximately:
#
#     mean = 0
#     standard deviation = 1
#
# This is particularly useful for neural networks because
# features with very different scales can make training harder.
scaler = StandardScaler()


# IMPORTANT:
# We fit the scaler ONLY on the training data.
#
# fit_transform():
# 1. learns the mean and standard deviation from X_train
# 2. scales X_train
X_train_scaled = scaler.fit_transform(X_train)


# For the test set, we ONLY transform the data.
#
# We must NOT call fit_transform() on X_test because that would
# leak information from the test set into the training process.
X_test_scaled = scaler.transform(X_test)


print(f"{X_train}\n")
print(f"{y_train}\n")


# ============================================================
# 3. CONVERT NUMPY ARRAYS TO PYTORCH TENSORS
# ============================================================

# Convert the NumPy feature arrays into PyTorch tensors.
#
# .float() converts the tensors to float32, which is the
# standard data type used by neural networks in PyTorch.
X_train_scaled_tensor = torch.from_numpy(X_train_scaled).float()
X_test_scaled_tensor = torch.from_numpy(X_test_scaled).float()


# Convert the target labels to PyTorch tensors.
#
# .float() is required because BCELoss expects floating-point
# target values (0.0 or 1.0).
#
# .unsqueeze(1) changes the shape from:
#
#     [batch_size]
#
# to:
#
#     [batch_size, 1]
#
# This matches the output shape of our neural network.
y_train_tensor = torch.from_numpy(y_train).float().unsqueeze(1)
y_test_tensor = torch.from_numpy(y_test).float().unsqueeze(1)


# ============================================================
# 4. CREATE A DATASET AND DATA LOADER
# ============================================================

# TensorDataset associates each input X with its corresponding
# target y.
train_dataset = TensorDataset(
    X_train_scaled_tensor,
    y_train_tensor
)


# DataLoader allows us to train the model using mini-batches.
#
# batch_size=32 means that the model processes 32 samples
# at a time.
#
# shuffle=True randomly changes the order of the training data
# at the beginning of each epoch.
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)


# ============================================================
# 5. DEFINE THE NEURAL NETWORK
# ============================================================

class BCNet(nn.Module):

    def __init__(self):
        super(BCNet, self).__init__()

        # First fully connected layer.
        #
        # Input:
        #     30 features
        #
        # Output:
        #     64 neurons
        self.fc1 = nn.Linear(30, 64)

        # Second fully connected layer.
        #
        # 64 inputs -> 32 outputs
        self.fc2 = nn.Linear(64, 32)

        # Output layer.
        #
        # 32 inputs -> 1 output
        #
        # The single output represents the probability
        # of belonging to class 1.
        self.fc3 = nn.Linear(32, 1)


    def forward(self, x):

        # Pass the input through the first layer
        # and apply the ReLU activation function.
        x = F.relu(self.fc1(x))

        # Pass the result through the second layer
        # and apply ReLU again.
        x = F.relu(self.fc2(x))

        # Pass the result through the output layer.
        #
        # Sigmoid converts the output into a value between 0 and 1.
        # This can be interpreted as a probability for binary
        # classification.
        x = F.sigmoid(self.fc3(x))

        return x


# ============================================================
# 6. CREATE THE MODEL, LOSS FUNCTION AND OPTIMIZER
# ============================================================

# BCELoss = Binary Cross Entropy Loss.
#
# It measures how different the predicted probabilities are
# from the actual binary labels (0 or 1).
criterion = nn.BCELoss()


# Create an instance of our neural network.
model = BCNet()


# Adam updates the model's weights using the gradients computed
# during backpropagation.
#
# lr = learning rate.
# It controls how large each update to the weights will be.
optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)


# Number of complete passes through the training dataset.
epochs = 20


# ============================================================
# 7. TRAINING LOOP
# ============================================================

for epoch in range(epochs):

    # Put the model in training mode.
    model.train()

    # Keep track of the total loss for this epoch.
    running_loss = 0.0


    # Iterate over the mini-batches provided by the DataLoader.
    for x_batch, y_batch in train_loader:

        # Clear the gradients from the previous iteration.
        #
        # PyTorch accumulates gradients by default, so we need
        # to reset them before computing new gradients.
        optimizer.zero_grad()


        # Forward pass:
        # Send the input batch through the neural network.
        preds = model(x_batch)


        # Calculate the difference between predictions
        # and the true labels.
        loss = criterion(preds, y_batch)


        # Backward pass:
        # Compute the gradients of the loss with respect
        # to all trainable parameters.
        loss.backward()


        # Update the model's weights using the gradients.
        optimizer.step()


        # Add this batch's loss to the running total.
        running_loss += loss.item()


    # Display the average loss for the current epoch.
    print(
        f"Epoch {epoch+1}: "
        f"Loss was {running_loss / len(train_loader)}"
    )


# ============================================================
# 8. EVALUATION
# ============================================================

# We don't need gradients during evaluation because we are
# not updating the model's parameters.
#
# This saves memory and computation.
with torch.no_grad():

    # Put the model in evaluation mode.
    model.eval()


    # Run the entire test set through the model.
    preds = model(X_test_scaled_tensor)


    # Calculate the test loss.
    loss = criterion(
        preds,
        y_test_tensor
    ).item()


    # Convert probabilities into binary predictions.
    #
    # Example:
    #
    # probability >= 0.5 -> class 1
    # probability <  0.5 -> class 0
    #
    # Then compare predictions with the true labels.
    #
    # .float() converts True/False into 1.0/0.0.
    # .mean() calculates the proportion of correct predictions.
    accuracy = (
        ((preds >= 0.5) == y_test_tensor)
        .float()
        .mean()
        .item()
    )


    print(accuracy)
