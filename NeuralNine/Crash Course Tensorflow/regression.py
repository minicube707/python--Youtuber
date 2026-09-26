import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ============================================================
# LOAD THE DATASET
# ============================================================

# Load the housing dataset from a CSV file.
#
# The dataset contains several features describing houses
# and a target variable called "MedHouseVal".
df = pd.read_csv('housing.csv')


# Display the complete DataFrame.
print(df)


# ============================================================
# PREPARE FEATURES AND TARGET
# ============================================================

# StandardScaler will standardize the input features.
#
# Each feature will approximately have:
#
#     mean = 0
#     standard deviation = 1
#
# This is useful for neural networks because the input features
# may have very different scales.
scaler = StandardScaler()


# Separate the input features (X) from the target (y).
#
# X = all columns except "MedHouseVal"
# y = "MedHouseVal"
#
# axis=1 means that we are dropping a column.
X, y = df.drop('MedHouseVal', axis=1), df['MedHouseVal']


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

# Split the dataset into:
#
#     80% -> training data
#     20% -> test data
#
# The model will learn from the training data and will later
# be evaluated on the test data.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)


# ============================================================
# STANDARDIZE THE FEATURES
# ============================================================

# Learn the mean and standard deviation from the training data
# and use them to scale X_train.
#
# IMPORTANT:
# We only "fit" the scaler on the training data.
X_train_scaled = scaler.fit_transform(X_train)


# Apply the same transformation to the test data.
#
# We use transform(), NOT fit_transform().
#
# This prevents information from the test set from leaking
# into the training process.
X_test_scaled = scaler.transform(X_test)


# Display the scaled training data.
print(f"{X_train_scaled=}")


# Display its shape.
#
# Expected:
#
#     (number_of_training_samples, 8)
#
# because the model expects 8 input features.
print(f"{X_train_scaled.shape=}")


# ============================================================
# BUILD THE NEURAL NETWORK
# ============================================================

# Sequential means that the layers are connected sequentially.
model = Sequential()


# First Dense layer:
#
#     8 input features -> 64 neurons
#
# ReLU introduces non-linearity into the network.
model.add(
    Dense(
        64,
        activation='relu',
        input_shape=(8,)
    )
)


# Second hidden layer:
#
#     64 neurons -> 64 neurons
#
# Again, we use ReLU as the activation function.
model.add(
    Dense(
        64,
        activation='relu'
    )
)


# Output layer:
#
#     64 neurons -> 1 output
#
# There is NO activation function here.
#
# This is important for regression because the network needs
# to be able to output a continuous numerical value.
#
# For example:
#
#     1.52
#     2.83
#     4.17
#     ...
model.add(
    Dense(1)
)


# ============================================================
# COMPILE THE MODEL
# ============================================================

# Compile the model before training.
#
# optimizer='adam':
#     Adam is used to update the neural network's weights.
#
# loss='mse':
#     Mean Squared Error measures the difference between
#     predicted and actual values.
#
# metrics:
#     MAE  -> Mean Absolute Error
#     R²   -> coefficient of determination
model.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae', 'r2_score']
)


# ============================================================
# TRAIN THE MODEL
# ============================================================

# Train the model for 10 complete passes through the
# training dataset.
model.fit(
    X_train_scaled,
    y_train,
    epochs=10
)


# ============================================================
# EVALUATE THE MODEL
# ============================================================

# Evaluate the trained model on the test set.
#
# The model has NOT seen these samples during training.
#
# This returns:
#
#     test loss (MSE)
#     test MAE
#     test R²
model.evaluate(
    X_test_scaled,
    y_test
)


# ============================================================
# MAKE A PREDICTION
# ============================================================

# Predict the target value for the first test sample.
#
# X_test_scaled[:1] means:
#     take only the first test sample.
#
# The output is a continuous numerical value.
print(
    f"\nPrediction: {model(X_test_scaled[:1])}"
)


# Display the real target value for comparison.
print(
    f"True value: {y_test[:1]}"
)


# ============================================================
# UNDERSTAND THE TARGET DISTRIBUTION
# ============================================================

# Display descriptive statistics for the target variable.
#
# This gives us information such as:
#
#     count
#     mean
#     standard deviation
#     minimum
#     25th percentile
#     median
#     75th percentile
#     maximum
#
# This is useful for understanding the scale and distribution
# of the values the model is trying to predict.
print(
    df.MedHouseVal.describe()
)
