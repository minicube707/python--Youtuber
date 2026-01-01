import bs4 as bs
import datetime as dt
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import numpy as np
import requests
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

style.use("ggplot")

def save_500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers)
    soup = bs.BeautifulSoup(resp.text, "lxml")

    table = soup.find("table", class_="wikitable")

    if table is None:
        raise Exception("Could not find the table. Page structure may have changed.")

    tickers = []
    for row in table.find_all("tr")[1:]:
        ticker = row.find_all("td")[0].text.strip()
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

#save_500_tickers()

def get_data_from_yahoo(reload_sp500=False):

    if reload_sp500:
        tickers = save_500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    
    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    start = "2000-01-01"
    end = dt.datetime.now().strftime("%Y-%m-%d")

    #The first 50
    for ticker in tickers[:50]:
        print(ticker)
        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            df = yf.download(ticker, start=start, end=end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

#get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers[:50]):
        df = pd.read_csv(
            f'stock_dfs/{ticker}.csv',
            header=[0, 1],
            index_col=0
        )

        # Aplatir les colonnes (Close, Open, etc.)
        df.columns = df.columns.get_level_values(0)

        # S'assurer que l'index est bien une date
        df.index = pd.to_datetime(df.index)

        # Renommer Close en nom du ticker
        df.rename(columns={'Close': ticker}, inplace=True)

        # Supprimer les colonnes inutiles
        df.drop(columns=['Open', 'High', 'Low', 'Volume'], inplace=True)

        # Construire le DataFrame principal
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


#compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')

    df_corr = df.corr()
    print(df_corr)

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_label = df_corr.columns
    rows_label = df_corr.index

    ax.set_xticklabels(column_label)
    ax.set_yticklabels(rows_label)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()

visualize_data()