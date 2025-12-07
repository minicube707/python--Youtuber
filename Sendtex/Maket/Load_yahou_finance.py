import json
import pandas as pd
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

# Charger le fichier JSON (local ou provenant d'une API)

name = "AMZON"
with open(name + ".json", 'r') as file:
    data = json.load(file)

# Étape 2 : Décoder le champ 'body' (il contient un JSON encodé sous forme de texte)
body_data = json.loads(data['body'])  # Décoder le contenu de 'body'

# Étape 3 : Extraire les données pertinentes
chart_data = body_data['chart']['result'][0]  # Premier élément de 'result'

# Métadonnées (infos sur l'action)
meta = chart_data['meta']
print(f"Symbole : {meta['symbol']}, Devise : {meta['currency']}")
print(f"Prix actuel : {meta['regularMarketPrice']}, Volume : {meta['regularMarketVolume']}")

# Timestamps et indicateurs (open, close, high, low, volume)
timestamps = chart_data['timestamp']  # Liste des timestamps
indicators = chart_data['indicators']['quote'][0]  # Indicateurs financiers

# Étape 4 : Convertir en DataFrame
df = pd.DataFrame({
    "timestamp": timestamps,
    "Open": indicators['open'],
    "Close": indicators['close'],
    "High": indicators['high'],
    "Low": indicators['low'],
    "Volume": indicators['volume'],
    "Adj Close":chart_data['indicators']['adjclose'][0]['adjclose']
})

# Convertir les timestamps en dates lisibles
df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
del df['timestamp']

df = df.rename(columns={'date': 'Date'})
df = df[['Date', 'Open', 'High', 'Low', 'Close', "Adj Close", 'Volume']]


# Afficher le DataFrame
print(df)

df.to_csv(name +'.csv', index=False, header=False, sep=',')

