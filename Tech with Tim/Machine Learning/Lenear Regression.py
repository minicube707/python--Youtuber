import pandas as pd
import numpy as np
import os
from sklearn import linear_model, model_selection
import pickle

os.chdir("Desktop\Document\Programme\Python\Youtuber\Tech with Tim\Machine Learning")
data = pd.read_csv("student-mat.csv", sep=";")

data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
print(data)

predict = "G3"

#Data without G3
X = np.array(data.drop([predict], 1))

#Only G3
y = np.array(data[predict])

x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size= 0.2)

#Create the model
linear = linear_model.LinearRegression()

#Train the model
linear.fit(x_train, y_train)

#Test the model
acc = linear.score(x_test, y_test)
print("Accurency ", acc)

#Coefficient
print("CO: \n", linear.coef_)
print("Intercept: \n",  linear.intercept_)

#Save the model
with open("studentmodel.pickle", "wb") as f:
    pickle.dump(linear, f)

#Read the model
pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)

predication =  linear.predict(x_test)

print("")
for x in range(len(predication)):
    print(predication[x], x_test[x], y_test[x])


