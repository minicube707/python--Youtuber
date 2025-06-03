from sklearn.datasets import load_breast_cancer
from sklearn import svm, model_selection
from sklearn.metrics import accuracy_score

cancer = load_breast_cancer()

#print(cancer.feature_names)
#print(cancer.target_names)

X = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size= 0.2)

classes = ['malignant' 'benign']

clf = svm.SVC(kernel = "linear")
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)

acc = accuracy_score(y_test, y_pred)
print(acc)