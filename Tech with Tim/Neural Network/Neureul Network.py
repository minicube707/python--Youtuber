from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", 'Ankle boot']

#Shrink the value of dataset
train_images = train_images / 255
test_images = test_images / 255

#Show an image of dataset
#plt.figure()
#plt.imshow(train_images[7], cmap=plt.cm.binary)
#plt.show()

#Set the model
model = keras.Sequential([
    keras.layers.Flatten(input_shape = (28, 28)),
    keras.layers.Dense(128, activation = "relu"), 
    keras.layers.Dense(10, activation = "softmax")])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])


#Train the model
model.fit(train_images, train_labels, epochs=5)

prediction = model.predict(test_images)

for i in range(5):
    plt.figure()
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel("Actual: " +  class_names[test_labels[i]])
    plt.title("Prediction: " + class_names[np.argmax(prediction[i])])
    plt.show()
