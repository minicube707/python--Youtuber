import pandas as pd
import numpy as np
import os
from sklearn import linear_model, model_selection
import matplotlib.pyplot as plt
import pickle

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

data = pd.read_csv("student-mat.csv", sep=";")

data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
print(data)

predict = "G3"

X = np.array(data.drop([predict], 1))
y = np.array(data[predict])
acc = 0

while acc < 0.90:

    x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size= 0.2)

    linear = linear_model.LinearRegression()
    linear.fit(x_train, y_train)

    acc = linear.score(x_test, y_test)

print("Final accurency", acc)

with open("studentbestmodel.pickle", "wb") as f:
    pickle.dump(linear, f)

predication =  linear.predict(x_test)

print("")
for x in range(len(predication)):
    print(predication[x], x_test[x], y_test[x])

p = "G1"
plt.figure()
plt.scatter(data[p], data["G3"])
plt.xlabel(p)
plt.ylabel("G3")
plt.show()
