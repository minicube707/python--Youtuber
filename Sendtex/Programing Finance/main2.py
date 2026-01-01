import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

def candle(ax1, date, open, close, hight, low, width = .3, width2 = .03, col1 = 'g', col2 = 'r'):

    # "up" dataframe will store the stock_prices  
    # when the closing stock price is greater 
    # than or equal to the opening stock prices 
    up = close >= open

    # "down" dataframe will store the stock_prices 
    # when the closing stock price is 
    # lesser than the opening stock prices 
    down = close < open
    
    # Plotting down prices of the stock 
    ax1.bar(date[down], close[down]-open[down], width, bottom=open[down], color=col2) 
    ax1.bar(date[down], hight[down]-open[down], width2, bottom=open[down], color=col2) 
    ax1.bar(date[down], low[down]-close[down], width2, bottom=close[down], color=col2) 

    # Plotting up prices of the stock 
    ax1.bar(date[up], close[up]-open[up], width, bottom=open[up], color=col1) 
    ax1.bar(date[up], hight[up]-close[up], width2, bottom=close[up], color=col1) 
    ax1.bar(date[up], low[up]-open[up], width2, bottom=open[up], color=col1) 

style.use("ggplot")

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

df = pd.read_csv("TSLA.csv", header=[0, 1] , index_col=0) # <-- two header rows

#Drop the ticker level in columns
df.columns = df.columns.droplevel(1)

#Remove junk rows and set Date index
df.index = pd.to_datetime(df.index)
df = df.apply(pd.to_numeric, errors="coerce")


df.index = pd.to_datetime(df.index)
df_ohlc =  df["Close"].resample('10D').ohlc()
df_volume = df["Volume"].resample('10D').sum()

print(df_ohlc.head())
df_ohlc.reset_index(inplace=True)
df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

ax1 =  plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 =  plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candle(ax1, date=df_ohlc["Date"], open=df_ohlc["open"], close=df_ohlc["close"], hight=df_ohlc["high"], low=df_ohlc["low"], width=10, width2=6)
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()