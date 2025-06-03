import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing, model_selection
import os

os.chdir("Desktop\Document\Programme\Python\Youtuber\Tech with Tim\Machine Learning")
data = pd.read_csv("car.data", sep=",")

print(data)

a = preprocessing.LabelEncoder()
buying = a.fit_transform(list(data["buying"]))
maint = a.fit_transform(list(data["maint"]))
door = a.fit_transform(list(data["door"]))
persons = a.fit_transform(list(data["persons"]))
lug_boot = a.fit_transform(list(data["lug_boot"]))
safety = a.fit_transform(list(data["safety"]))
cls = a.fit_transform(list(data["class"]))

print(buying)

predict =  "class"

X = list(zip(buying, maint, door, persons, lug_boot, safety))
y = list(cls)

x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size= 0.2)

model = KNeighborsClassifier(n_neighbors= 5)
model.fit(x_train, y_train)
acc = model.score(x_test, y_test)
print("Accurency ", acc)

predictited = model.predict(x_test)
names = ["unacc", "acc", "godd", "very good"]

for x in range(len(x_test)):
    print("Predicticted: ", names[predictited[x]], "\tData: ", x_test[x], "\tActual: ", names[y_test[x]])
    n = model.kneighbors([x_test[x]], 5, True)
    print("N: ", n)