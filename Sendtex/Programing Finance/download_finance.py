import yfinance as yf
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

ticker = "AXON"
start_date = "2010-01-01"
end_date = None  # jusqu'à aujourd'hui

# Télécharger les données
df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    progress=False
)
# Sauvegarder en CSV
df.to_csv(f"{ticker}.csv")

print(f"{ticker}.csv téléchargé avec succès")
