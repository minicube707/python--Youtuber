import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from datetime import datetime

module_dir = os.path.dirname(__file__)
os.chdir(os.path.join(module_dir, "Data"))

# Fonction de conversion pour convertir une chaîne de caractères en objet date
def convert_date(date_str):
    return datetime.strptime(date_str.decode('utf-8'), "%Y-%m-%d")


def lister_fichiers_csv():
    
    # Récupère le dossier courant (répertoire où le script est exécuté)
    dossier_courant = os.getcwd()

    # Liste pour stocker les fichiers CSV trouvés
    fichiers_csv = []

    # Parcours des fichiers dans le dossier courant
    for fichier in os.listdir(dossier_courant):
        # Vérifie si le fichier est un fichier .csv
        if fichier.endswith(".csv"):
            fichiers_csv.append(fichier[:-4])

    # Affiche les fichiers CSV trouvés
    if fichiers_csv:
        print("Fichiers CSV trouvés :")
        for fichier in fichiers_csv:
            print(fichier)
    else:
        print("Aucun fichier CSV trouvé dans le dossier actuel.")


def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    donw = -seed[seed<0].sum()/n
    rs = up/donw
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1 + rs)

    for i in range(len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        
        else:
            upval = 0.
            downval = - delta
    
        up = (up*(n-1) + upval)/n
        donw = (donw*(n-1) + downval)/n

        rs = up/donw
        rsi[i] = 100. - 100./(1. + rs)
    
    return rsi

def movingaverage(values, window):
    weight = np.repeat(1.0, window)/window
    smas = np.convolve(values, weight, "valid")
    return smas

def ExpMovingAverage(value, window):
    weight = np.exp(np.linspace(-1., 0, window))
    weight /= weight.sum()
    a = np.convolve(value, weight, mode="full")[:len(value)]
    a[:window] = a[window]
    return a

def computeMACD(x, slow=26, fast=12):
    """
    macd line = 12ema - 26ema
    signal line = 9ema of the macd line
    histogram = mad line - signal line
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast-emaslow

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
        years_mask = years >= (current_year - 10)

        Date = Date[years_mask]
        Open = Open[years_mask]
        High = High[years_mask]
        Low = Low[years_mask]
        Close = Close[years_mask]
        Volume = Volume[years_mask]

        Av1 = movingaverage(Close, MA1)
        Av2 = movingaverage(Close, MA2)
        SP = len(Date[MA2 -1:])
        labal1 = str(MA1) + " SMA"
        labal2 = str(MA2) + " SMA"

        fig = plt.figure(figsize=(10, 8), facecolor="k")
        plt.suptitle(stock + " Stock Price", color="w")


        #Mid graph
        ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
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
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune="upper"))
        ax1.spines["bottom"].set_color("royalblue")
        ax1.spines["top"].set_color("royalblue")
        ax1.spines["right"].set_color("royalblue")
        ax1.spines["left"].set_color("royalblue")
        ax1.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax1.set_ylabel("Stock Price", color="w")
        ax1.set_xlabel("Date", color="w")
        plt.legend(facecolor='grey', fancybox= True, prop={"size":9}, labelcolor="k")

        #Volume
        VolumeMin = 0
        ax1v = ax1.twinx()
        ax1v.fill_between(Date[-SP:],VolumeMin, Volume[-SP:], facecolor="#1F77B4", alpha=.5)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.spines["bottom"].set_color("royalblue")
        ax1v.spines["top"].set_color("royalblue")
        ax1v.spines["right"].set_color("royalblue")
        ax1v.spines["left"].set_color("royalblue")
        ax1v.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax1v.set_ylim(0, 3*Volume.max())
        ax1v.set_ylabel("Volume", color="w")


        #Top graph
        ax0 = plt.subplot2grid((6,4), (0, 0), rowspan=1, colspan=4, sharex=ax1)
        ax0.set_facecolor("k")

        #Show data
        rsi = rsiFunc(Close)
        ax0.plot(Date[-SP:], rsi[-SP:], color="#1F77B4", linewidth=1.5)
    
        #Comestic
        ax0.spines["bottom"].set_color("royalblue")
        ax0.spines["top"].set_color("royalblue")
        ax0.spines["right"].set_color("royalblue")
        ax0.spines["left"].set_color("royalblue")
        ax0.yaxis.set_ticks([])
        ax0.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax0.text(0.015, 0.95, "RSI (14)", va="top", color="w", transform=ax0.transAxes)
        ax0.set_ylim(0, 100)
        ax0.axhline(70, color="r")
        ax0.axhline(30, color="g")
        ax0.set_yticks([30, 70])
        ax0.fill_between(Date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:] >=70), facecolor="r", edgecolor="r")
        ax0.fill_between(Date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:] <=30), facecolor="g", edgecolor="g")
        #plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune="lower"))
        
        #Bit graph
        ax2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=ax1)
        ax2.set_facecolor("k")
        
        #Show data
        Slow = 26
        Fast = 12
        nema = 9
        emaslow, emafast, macd = computeMACD(Close)
        ema9 = ExpMovingAverage(macd, nema)

        ax2.plot(Date[-SP:], macd[-SP:], color="#4ee6fd", lw=2)
        ax2.plot(Date[-SP:], ema9[-SP:], color="#e1edf9", lw=1)
        ax2.fill_between(Date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor="#1F77B4", edgecolor="#1F77B4")
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune="upper"))

        #Cometic
        ax2.spines["bottom"].set_color("royalblue")
        ax2.spines["top"].set_color("royalblue")
        ax2.spines["right"].set_color("royalblue")
        ax2.spines["left"].set_color("royalblue")
        ax2.tick_params(axis='both', which='major', colors='w')  # Couleur blanc pour les ticks majeurs
        ax2.text(0.015, 0.95, f"MACD {Fast}, {Slow}, {nema}", va="top", color="w", transform=ax2.transAxes)
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune="upper"))

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        #Global Comestic
        plt.subplots_adjust(left=.12, bottom=.15 , right=.95, top=.95, wspace=.20, hspace=0)
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.xlim(Date[-SP:][0])
        plt.show()
        

 
    except Exception as e:
        print("failed main loop", str(e))

lister_fichiers_csv()
print("")
print("Please enter a stock")
Stock = input()
graphData(Stock, 20, 200)