import pandas as pd
import os 

os.chdir("Desktop\Document\Programmation\Python\Youtuber\Sendtex\Maket")

import pandas as pd

# Chargement du fichier CSV
data = pd.read_csv("TSLA.csv", sep="\t", decimal=",")

# Ajout des titres aux colonnes
data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

# Vérification
data["Date"] = data["Date"].str.split()

for date in data["Date"]:
    match date[1]:
        case "févr.":
           date[1] = "feb"
        
        case "avr.":
            date[1] = "apr"
        
        case "mai":
            date[1] = "may"
        
        case "juin":
            date[1] = "jun"
        
        case "juil.":
            date[1] = "jully"
        
        case "août":
            date[1] = "aug"
        
        case "déc.":
            date[1] = "dec"

    if len(date[1]) > 3:
        date[1] = date[1][:-len(date[1]) + 3]


for i in range(len(data["Date"])):
   data.loc[i, "Date"] = ' '.join(data.loc[i, "Date"])

# Conversion du format des dates
data["Date"] = pd.to_datetime(data["Date"], format="%d %b %Y")  # Format actuel: 11 déc. 2024

# Reformater les dates dans le format souhaité (YYYY-MM-DD)
data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

for i in range(len(data["Volume"])):
   data.loc[i, "Volume"] = data.loc[i, "Volume"][:-1].replace(",", ".")

data.insert(5, "Adj Close", data["Close"])
print(data)

data.to_csv('tsla.csv', sep=",", index=False)
    




