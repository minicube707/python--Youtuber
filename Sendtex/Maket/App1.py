import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from datetime import datetime

module_dir = os.path.dirname(__file__)
os.chdir(os.path.join(module_dir, "Data"))

eachStock ="TSLA"

# Fonction de conversion pour convertir une chaîne de caractères en objet date
def convert_date(date_str):
    return datetime.strptime(date_str.decode('utf-8'), "%Y-%m-%d")

def movingaverage(values, window):
    weight = np.repeat(1.0, window)/window
    smas = np.convolve(values, weight, "valid")
    return smas

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
    
def plot(ax1, Date, Open, High, Low, Close):
    ax1.plot(Date, Open, linewidth=.5)
    ax1.plot(Date, High, linewidth=.5)
    ax1.plot(Date, Low, linewidth=.5)
    ax1.plot(Date, Close, linewidth=.5)

def graphData(stock, MA1, MA2):
    try:
        stockFile = stock + ".csv"        
        Date, Open, High, Low, Close, Adj_Close, Volume = np.genfromtxt(stockFile, delimiter=",", unpack=True, skip_header=1, converters={0: convert_date})

        years = np.array([date.year for date in Date])
        current_year = datetime.now().year
        years_mask = years >= (current_year - 1)

        Date = Date[years_mask]
        Open = Open[years_mask]
        High = High[years_mask]
        Low = Low[years_mask]
        Close = Close[years_mask]
        Volume = Volume[years_mask]
        VolumeMin = 0

        Av1 = movingaverage(Close, MA1)
        Av2 = movingaverage(Close, MA2)
        SP = len(Date[MA2 -1:])
        labal1 = str(MA1) + " SMA"
        labal2 = str(MA2) + " SMA"

        fig = plt.figure(figsize=(10, 8), facecolor="k")
        plt.suptitle(stock + " Stock Price", color="w")
        
        #Top graph
        ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4)
        ax1.set_facecolor("k")

        #Show data
        #plot(ax1, Date, Open, High, Low, Close)
        candle(ax1, Date[-SP:], Open[-SP:], Close[-SP:], High[-SP:], Low[-SP:], 3, .5)
        ax1.plot(Date[-SP:], Av1[-SP:], label=labal1, color="lime")
        ax1.plot(Date[-SP:], Av2[-SP:], label=labal2, color="cyan")

        #Comestic
        ax1.grid(True, color="w", linestyle='--')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m -%d"))
        ax1.spines["bottom"].set_color("royalblue")
        ax1.spines["top"].set_color("royalblue")
        ax1.spines["right"].set_color("royalblue")
        ax1.spines["left"].set_color("royalblue")
        ax1.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax1.set_ylabel("Stock Price", color="w")
        plt.legend(facecolor='grey', fancybox= True, prop={"size":9}, labelcolor="k")
        

        #Bot graph
        ax2 = plt.subplot2grid((5, 4), (4, 0), rowspan=1, colspan=4, sharex=ax1)
        ax2.set_facecolor("k")

        #Show data
        ax2.plot(Date, Volume, linewidth=.5)

        #Comestic
        ax2.fill_between(Date,VolumeMin, Volume, facecolor="#1F77B4", alpha=.5)
        ax2.axes.yaxis.set_ticklabels([])
        ax2.grid(True, color="w", linestyle='--')
        ax2.spines["bottom"].set_color("royalblue")
        ax2.spines["top"].set_color("royalblue")
        ax2.spines["right"].set_color("royalblue")
        ax2.spines["left"].set_color("royalblue")
        ax2.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax2.set_ylabel("Volume", color="w")
        ax2.set_xlabel("Date", color="w")

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        #Global Comestic
        plt.subplots_adjust(left=.12, bottom=.15 , right=.95, top=.95, wspace=.20, hspace=0)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.show()
        

 
    except Exception as e:
        print("failed main loop", str(e))

graphData(eachStock, 12, 26)