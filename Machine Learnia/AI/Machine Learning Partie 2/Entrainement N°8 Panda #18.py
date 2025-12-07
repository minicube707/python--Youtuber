import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)
os.chdir("../Data")

bitcoin = pd.read_csv('BTC-EUR.csv')

print("Voici le fichier BTC-EUR.csv")
print(bitcoin)

print("")
print("Voici la première partie du fichier BTC-EUR.csv")
print(bitcoin.head())

plt.figure()
bitcoin['Close'].plot()
plt.title("Evolution du bitcion en fonction des indices")
plt.show()

print("")
print("Les index sont :")
print(bitcoin.index)

#//////////////////////////////////////////////////////////////////

#Inclusion des dates
print("")
print("#Inclusion des dates")

#index_col='Date':
#Cela indique à Pandas d'utiliser la colonne "Date" du fichier CSV comme index du DataFrame résultant.
#L'index est utilisé pour accéder aux lignes du DataFrame de manière plus conviviale et pour effectuer des opérations d'alignement.

#parse_dates=True:
#Cette option indique à Pandas de tenter de convertir les valeurs de la colonne "Date" en objets de date/heure,
#ce qui est utile pour travailler avec des séries temporelles.
#Si les dates sont correctement formatées dans le fichier CSV,
#cette option vous permettra de manipuler facilement les données temporelles.

bitcoin = pd.read_csv('BTC-EUR.csv', index_col='Date', parse_dates=True )

print("Voici le fichier BTC-EUR.csv")
print(bitcoin)

print("")
print("Voici la première partie du fichier BTC-EUR.csv")
print(bitcoin.head())

plt.figure()
bitcoin['Close'].plot()
plt.title("Evolution du bitcion en fonction des dates")
plt.show()

print("")
print("Les index sont :")
print(bitcoin.index)

#//////////////////////////////////////////////////////////////////

#Dates

print("")
print("#Dates")

plt.figure()
bitcoin.loc['2019']['Close'].plot()
plt.title("Evolution du bitcion en 2019")
plt.show()

plt.figure()
bitcoin.loc['2019-09']['Close'].plot()
plt.title("Evolution du bitcion en Septembre 2019")
plt.show()

plt.figure()
bitcoin.loc['2016':'2019']['Close'].plot()
plt.title("Evolution du bitcion entre 2016 et 2019")
plt.show()

#resample()
#Regroupe les données selon une données temporelle
plt.figure()
bitcoin.loc['2019']['Close'].resample('M').plot()
plt.title("Evolution du bitcion en 2019 regroupé par mois")
plt.show()

plt.figure()
bitcoin.loc['2019-09']['Close'].resample('W').plot()
plt.title("Evolution du bitcion en Septembre 2019 regroupé par semaine")
plt.show()

plt.figure()
bitcoin.loc['2019-09']['Close'].resample('2W').plot()
plt.title("Evolution du bitcion en Septembre 2019 regroupé toutes les deux semaines")
plt.show()

plt.figure()
bitcoin.loc['2019']['Close'].resample('M').mean().plot()
plt.title("Evolution de la moyenne du bitcion en 2019 ")
plt.show()



plt.figure(figsize=(12,8))
bitcoin.loc['2019']['Close'].plot()
bitcoin.loc['2019']['Close'].resample('M').mean().plot(label='moyenne par mois', lw=3, ls=':', alpha=0.8)
bitcoin.loc['2019']['Close'].resample('W').mean().plot(label='moyenne par semaine', lw=2, ls='--', alpha=0.8)
bitcoin.loc['2019']['Close'].resample('2W').mean().plot(label='moyenne toutes les deux semaines', lw=2, ls='-', alpha=0.5)
plt.title("Graphique des moyennes du bitcoins en 2019")
plt.legend()
plt.show()


#//////////////////////////////////////////////////////////////////

#AGG
#.agr([])
#Rassemble dans un seul tableau plusieurs statistique pae dessus resample()
print("")
print("#AGG")

print("")
print("Tableau sur la moyenne, l'écart type, le min & le max du cours du bitcion en 2019")
print(bitcoin.loc['2019']['Close'].resample('W').agg(['mean','std','min','max']))

bitcoin.loc['2019', 'Close'].resample('W').agg(['mean', 'std', 'min', 'max']).plot()
plt.title("Tableau sur la moyenne, l'écart type, le min & \nle max du cours du bitcion en 2019")
plt.show()

plt.figure(figsize=(12,8))
bitcoin.loc['2019-09', 'Close'].plot()
bitcoin.loc['2019-09', 'Close'].rolling(window=7).mean().plot(label='moving average', lw=3, ls=':',alpha=0.5)
bitcoin.loc['2019-09', 'Close'].rolling(window=7,center=True).mean().plot(label='moving average in middle', lw=2, ls='--',alpha=0.4)
bitcoin.loc['2019-09', 'Close'].ewm(alpha=0.5).mean().plot(label='Exponenteil weighted mobile', lw=2, ls=':',alpha=0.6)
plt.title("La moyenne tous les septs jours en 2019")
plt.legend()
plt.show()

plt.figure(figsize=(12,8))
bitcoin.loc['2019-09', 'Close'].plot()
for i in np.arange(0.2, 1, 0.2):
    bitcoin.loc['2019-09', 'Close'].ewm(alpha=i).mean().plot(label= f' alpha= {i}', lw=2, ls=':',alpha=0.5)
plt.title("Graphique avec les variations de alpha")
plt.legend()
plt.show()

#//////////////////////////////////////////////////////////////////

#Etherium
print("")
print("#Etherium")

etherium = pd.read_csv('ETH-EUR.csv', index_col='Date', parse_dates=True )

print("Voici le fichier ETH-EUR.csv")
print(etherium)

print("")
print("Voici la première partie du fichier ETH-EUR.csv")
print(etherium.head())

plt.figure()
etherium['Close'].plot()
plt.title("Evolution du etherium en fonction des dates")
plt.show()

print("")
print("Les index sont :")
print(etherium.index)

plt.figure()
bitcoin['Close'].plot(label='bitcoin')
etherium['Close'].plot(label='etherium')
plt.title("Comparaison entre le bitcoin et l'étherium")
plt.legend()
plt.show()

#on
#paramétre sur lequel on indique sur quelle  colonne nos données doivent s'aligner

#how
#paramétre indiquant la façon dont nos données vont s'aligner
print('')
print("Tableau sur le bitcoin et l'étherium")
print(pd.merge(bitcoin, etherium, on='Date', how='outer'))

print('')
print("Tableau sur le bitcoin et l'étherium sur leurs années communes ")
print(pd.merge(bitcoin, etherium, on='Date', how='inner'))

#suffixes()
#Paramétre permetant de changer le sufixe x,y par le sufixe que l'on veut
tab_eth_bitc=pd.merge(bitcoin, etherium, on='Date', how='inner',suffixes=('_btc','_eth'))
print('')

print("Tableau sur le bitcoin et l'étherium ")
print(tab_eth_bitc)


tab_eth_bitc[['Close_btc','Close_eth']].plot()
plt.title("Comparaison entre le bitcoin et l'étherium sur les même dates")
plt.show()

#subplots()
#Permet de séparer les n graphiques en n sous graphique
tab_eth_bitc[['Close_btc','Close_eth']].plot(subplots=True)
plt.title("Comparaison entre le bitcoin et l'étherium sur les même dates")
plt.show()

print("")
print("Tableau de corelation")
print(tab_eth_bitc[['Close_btc','Close_eth']].corr())


#//////////////////////////////////////////////////////////////////

#Exercice
print('')
print('#Exercice')

#shift()
#Cette méthode est utilisée pour décaler les données temporelles (graphe) vers la droite (ou vers la gauche) d'un nombre de pas définie.
#Dans cet exemple, nous décalons les données d'une période vers la droite.

#.rolling(window=28):
#Cette méthode crée une fenêtre de déroulement de largeur 28.
#Cela signifie qu'à chaque étape, la fenêtre couvrira les 28 dernières valeurs de la série.
#Cela est souvent utilisé pour effectuer des calculs de moyennes mobiles ou d'autres calculs similaires sur une série temporelle.
#Ici rolling() permet de calculer le min et max des 28 jours précédant
max=bitcoin.loc['2018-12':'2019', 'Close'].shift(1).rolling(window=28).max()
min=bitcoin.loc['2018-12':'2019', 'Close'].shift(1).rolling(window=28).min()

btc_trade = bitcoin.loc['2019'].drop(['Open','High','Low','Adj Close','Volume'],axis=1)
btc_trade_buy = btc_trade.copy()
btc_trade_sell = btc_trade.copy()

fus1=pd.merge(btc_trade, max, on='Date', how='inner',suffixes=('','_max'))
fus2=pd.merge(fus1, min, on='Date', how='inner',suffixes=('','_min'))

mask_max=fus2['Close']>fus2['Close_max']
mask_min=fus2['Close']<fus2['Close_min']

print('')
print('mask_max')
print(mask_max)

print('')
print('mask_min')
print(mask_min)

fus2.plot()
plt.legend()
plt.show()

print('')
print('btc_trade')
print(btc_trade)

btc_trade_buy['Buy']=np.zeros(len(bitcoin['2019']))
btc_trade_sell['Sell']=np.zeros(len(bitcoin['2019']))

print('')
print('btc_trade_buy')
print(btc_trade_buy)

print('')
print('btc_trade_sell')
print(btc_trade_sell)

btc_trade_buy=btc_trade_buy.loc['2019'].drop(['Close'],axis=1)
btc_trade_sell=btc_trade_sell.loc['2019'].drop(['Close'],axis=1)

print('')
print('btc_trade_buy')
print(btc_trade_buy)

print('')
print('btc_trade_sell')
print(btc_trade_sell)

btc_trade_buy[mask_max==True]=1
btc_trade_sell[mask_min==True]=-1

print('')
print('btc_trade_buy')
print(btc_trade_buy)

print('')
print('btc_trade_sell')
print(btc_trade_sell)

pd.merge(btc_trade_buy, btc_trade_sell,on='Date').plot()
plt.show()


fig, ax = plt.subplots(2, figsize=(12, 8), sharex=True)
ax[0].plot(fus2)
ax[0].legend(['close', 'max', 'min'])

ax[1].plot(pd.merge(btc_trade_buy, btc_trade_sell,on='Date'))
ax[1].legend(['buy', 'sell'])
plt.title("Exercice")

plt.show()

#//////////////////////////////////////////////////////////////////

#Correction
print("")
print("#Correction")

data = bitcoin.copy()
data['Buy'] = np.zeros(len(data))
data['Sell'] = np.zeros(len(data))
     
data['RollingMax'] = data['Close'].shift(1).rolling(window=28).max()
data['RollingMin'] = data['Close'].shift(1).rolling(window=28).min()
data.loc[data['RollingMax'] < data['Close'], 'Buy'] = 1
data.loc[data['RollingMin'] > data['Close'], 'Sell'] = -1
     
start ='2019'
end='2019'
fig, ax = plt.subplots(2, figsize=(12, 8), sharex=True)
#plt.figure(figsize=(12, 8))
#plt.subplot(211)
ax[0].plot(data['Close'][start:end])
ax[0].plot(data['RollingMin'][start:end])
ax[0].plot(data['RollingMax'][start:end])
ax[0].legend(['close', 'min', 'max'])
ax[1].plot(data['Buy'][start:end], c='g')
ax[1].plot(data['Sell'][start:end], c='r')
ax[1].legend(['buy', 'sell'])
plt.title("Correction")
plt.show()