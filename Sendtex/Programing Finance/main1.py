import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

style.use("ggplot")

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

df = pd.read_csv("TSLA.csv", parse_dates=True, index_col=0)

#Show the begining of the dataset
print(df.head())

#Display the dataset
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df["High"] = pd.to_numeric(df["Close"], errors="coerce")
df["Low"] = pd.to_numeric(df["Close"], errors="coerce")
df["Open"] = pd.to_numeric(df["Close"], errors="coerce")
df["Volume"] = pd.to_numeric(df["Close"], errors="coerce")
df.plot()
plt.show()

#Add a column
df['100ma'] = df["Close"].rolling(window=100, min_periods=0).mean()
df.dropna(inplace=True)

#Show the begining of the dataset
print("\n", df.head())

ax1 =  plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 =  plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df["Close"])
ax1.plot(df.index, df["100ma"])
ax2.bar(df.index, df["Volume"])

plt.show()