import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.preprocessing import OrdinalEncoder
import numpy as np
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

data = pd.read_csv("car.data", sep=",")
print(data)

enc = OrdinalEncoder()
processing_data = pd.DataFrame(enc.fit_transform(data))
print(processing_data)

predict = 6
model = KNeighborsClassifier(n_neighbors=10)

X = np.array(processing_data.drop([predict], 1))
y = np.array(processing_data[predict])

x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size= 0.2)

model.fit(x_train, y_train)
acc = model.score(x_test, y_test)
print(acc)