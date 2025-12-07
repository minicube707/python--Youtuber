import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import*
from sklearn.datasets import load_digits
from sklearn.linear_model import LinearRegression
import pandas as pd
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)
os.chdir("../Data")

#Importation du dataset sur le prix de l'immobilier de Boston
#data_url = "http://lib.stat.cmu.edu/datasets/boston"
#raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)

raw_df = pd.read_csv("boston_housing.csv")
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

#Comment calculer les erreurs de notre moldel 

#MAE est utile lorsque vous voulez une mesure d'erreur facile à interpréter et que les erreurs de prédiction ont une importance égale.
#MAE est une mesure de l'erreur qui calcule la moyenne des écarts absolus entre les prédictions d'un modèle et les valeurs réelles.

#MSE est utile lorsque vous voulez pénaliser davantage les erreurs importantes, ce qui peut être le cas dans certaines applications.
#MSE calcule la moyenne des carrés des écarts entre les prédictions du modèle et les valeurs réelles.

#RMSE est similaire à la MSE, mais fournit une mesure d'erreur dans l'unité d'origine, ce qui peut être plus intuitif.
#RMSE est une mesure de l'erreur qui est la racine carrée de la MSE.

#Exemple
print("Pour une valeur")
for i in range(0,5):
    y=np.array([2])
    y_pred=np.array([2+i])

    print("")
    print("MAE :", mean_absolute_error(y, y_pred))
    print("MSE :", mean_squared_error(y, y_pred))
    print("RMSE :", np.sqrt(mean_squared_error(y, y_pred)))

print("")
print("Pour deux valeurs")
for i in range(0,5):
    y=np.array([2, 4])
    y_pred=np.array([2+i, 4])

    print("")
    print("MAE :", mean_absolute_error(y, y_pred))
    print("MSE :", mean_squared_error(y, y_pred))
    print("RMSE :", np.sqrt(mean_squared_error(y, y_pred)))

digits =load_digits()
X=data
y=target

model=LinearRegression()
model.fit(X,y)
y_pred=model.predict(X)

plt.figure()
plt.scatter(X[:,5], y, label='y')
plt.scatter(X[:,5],y_pred, label="Y_pred")
plt.legend()
plt.show()

#L'histogramme des erreurs du model par une une MAE
err_hist=np.abs(y-y_pred)
plt.figure()
plt.title("L'histogramme des erreurs du model par une une MAE")
plt.hist(err_hist, bins=50)
plt.show()