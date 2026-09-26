import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam


# ============================================================
# TENSORFLOW VS KERAS
# ============================================================

# TensorFlow is a machine learning framework that provides
# low-level operations for tensors, automatic differentiation,
# GPU acceleration, and many other tools.
#
# Keras is a high-level deep learning API that makes it easier
# to build, train, and evaluate neural networks.
#
# Keras can run on top of TensorFlow and provides convenient
# abstractions such as:
#
#     Sequential
#     Dense
#     Dropout
#     model.compile()
#     model.fit()
#     model.evaluate()
#
# In modern TensorFlow, Keras is tightly integrated with
# TensorFlow and is usually the easiest way to build models.


# ============================================================
# LOAD THE MNIST DATASET
# ============================================================

# MNIST is a dataset of handwritten digits from 0 to 9.
#
# Each image is:
#
#     28 x 28 pixels
#
# There are:
#
#     60,000 training images
#     10,000 test images
#
mnist = tf.keras.datasets.mnist


# Load the training and test data.
#
# X = input images
# y = corresponding labels
#
# For example:
#
#     X_train[0] -> image of a handwritten digit
#     y_train[0] -> the corresponding digit (0 to 9)
(X_train, y_train), (X_test, y_test) = mnist.load_data()



# Display the shape of the training images.
#
# Expected:
#
#     (60000, 28, 28)
#
# This means:
#     60,000 images
#     28 rows
#     28 columns
print(f"\n{X_train.shape=}")


# Display the shape of the training labels.
#
# Expected:
#
#     (60000,)
#
# There is one label for each training image.
print(f"{y_train.shape=}")


# ============================================================
# NORMALIZE THE INPUT DATA
# ============================================================

# Pixel values in MNIST are integers between 0 and 255.
#
# Neural networks generally train better when input values
# are kept within a smaller range.
#
# Dividing by 255 transforms:
#
#     0   -> 0.0
#     255 -> 1.0
#
X_train, X_test = X_train / 255.0, X_test / 255.0


# ============================================================
# BUILD THE NEURAL NETWORK
# ============================================================

# Sequential means that the layers are connected one after
# another in a simple linear stack.
model = Sequential()


# Define the input shape.
#
# Each input image has:
#
#     28 rows x 28 columns
#
# We don't specify the batch size here because Keras handles
# the batch dimension automatically.
model.add(Input((28, 28)))


# Flatten converts the 2D image into a 1D vector.
#
# Before:
#
#     (28, 28)
#
# After:
#
#     (784,)
#
# because:
#
#     28 * 28 = 784
#
# This allows us to feed the image into fully connected
# (Dense) layers.
model.add(Flatten())


# Fully connected layer with 128 neurons.
#
# ReLU introduces non-linearity:
#
#     ReLU(x) = max(0, x)
#
# Without activation functions, stacking multiple Dense
# layers would still behave like a single linear transformation.
model.add(Dense(128, activation='relu'))


# Dropout randomly disables 20% of the neurons during training.
#
# This helps reduce overfitting by preventing the network
# from relying too heavily on specific neurons.
#
# Dropout is active during training but disabled during
# evaluation/inference.
model.add(Dropout(0.2))


# Final layer:
#
# 10 neurons = 10 possible classes:
#
#     0, 1, 2, ..., 9
#
# Notice that there is NO softmax activation here.
#
# The layer outputs raw scores called "logits".
model.add(Dense(10))


# ============================================================
# LOGITS VS PROBABILITIES
# ============================================================

# Run one image through the untrained model.
#
# X_train[:1] means:
#     take only the first image
#
# At this point the model has random weights, so the output
# is essentially a random prediction.
nonsense_prediction = model(X_train[:1]).numpy()


# These are the raw outputs from the final Dense layer.
#
# They are called logits.
#
# They are NOT probabilities.
#
# They can be positive or negative and do not have to add up
# to 1.
print(f"\nLogit: {nonsense_prediction}")


# Apply softmax to convert the logits into probabilities.
#
# Softmax ensures:
#
#     every value is between 0 and 1
#     all probabilities add up to 1
#
# Example:
#
#     [2.1, 0.5, -1.0, ...]
#
# becomes something like:
#
#     [0.65, 0.13, 0.03, ...]
#
# The highest probability corresponds to the model's
# predicted class.
print(
    f"Softmax: "
    f"{tf.nn.softmax(nonsense_prediction).numpy()}"
)


# ============================================================
# LOSS FUNCTION
# ============================================================

# SparseCategoricalCrossentropy is commonly used for
# multi-class classification when the labels are integers.
#
# Example:
#
#     y = 7
#
# instead of one-hot encoding:
#
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
#
# from_logits=True tells Keras that the model outputs
# raw logits rather than probabilities.
loss_fn = SparseCategoricalCrossentropy(
    from_logits=True
)


# ============================================================
# EXPECTED LOSS FOR A RANDOM GUESS
# ============================================================

# If the model assigns approximately the same probability
# to all 10 classes, each class has:
#
#     probability = 1 / 10
#
# The negative log likelihood is:
#
#     -log(1/10)
#
# which is approximately:
#
#     2.3026
#
expected_loss = -tf.math.log(1 / 10)

print(
    '\nExpected loss on random guess',
    expected_loss
)


# Calculate the actual loss produced by the randomly
# initialized model for the first training example.
#
# Because the model is untrained, this should be in the
# general neighborhood of the random-guess loss.
print(
    'Actual loss:',
    loss_fn(y_train[:1], nonsense_prediction)
)


# ============================================================
# COMPILE AND TRAIN THE MODEL
# ============================================================

# Adam is an optimization algorithm used to update the
# neural network's weights based on the gradients.
#
# learning_rate controls the size of each update.
optimizer = Adam(
    learning_rate=0.01
)


# Configure the model for training.
#
# optimizer:
#     defines how weights are updated
#
# loss:
#     defines what the model tries to minimize
#
# metrics:
#     defines what we want to monitor during training
model.compile(
    optimizer=optimizer,
    loss=loss_fn,
    metrics=['accuracy']
)


# Train the model.
#
# epochs=10 means that the complete training dataset
# is processed 10 times.
#
# During each epoch, Keras performs approximately:
#
#     forward pass
#          ↓
#        loss
#          ↓
#     backpropagation
#          ↓
#     gradient computation
#          ↓
#     optimizer update
#
model.fit(
    X_train,
    y_train,
    epochs=10
)


# ============================================================
# EVALUATE THE MODEL
# ============================================================

# Evaluate the trained model on data it has NOT seen
# during training.
#
# This returns the test loss and test accuracy.
model.evaluate(
    X_test,
    y_test
)


# ============================================================
# MAKE A PREDICTION
# ============================================================

# Run the first test image through the trained model.
#
# model(X_test[:1]) returns 10 logits.
#
# softmax converts the logits into probabilities.
prediction = tf.nn.softmax(
    model(X_test[:1])
)


# tf.argmax(..., axis=1) returns the index of the largest
# probability.
#
# Since the indices correspond to the digits 0-9, this gives
# us the predicted digit.
print(
    f"\nPrediction: "
    f"{tf.argmax(prediction, axis=1)}"
)


# Display the actual label of the image.
print(
    f"True value: {y_test[:1]}"
)
