import pandas as pd

deckcsv = pd.read_csv("deckcards.csv")
maindeck = deckcsv["CardID"].tolist()
