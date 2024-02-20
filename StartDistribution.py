import random
import pandas as pd

deckcsv = pd.read_csv("deckcards.csv")
maindeck = deckcsv["CardID"].tolist()


def startrole(playernum: int) -> dict:
    roles = ["Red", "Red", "Blue", "Blue", "Green"]
    if playernum == 6 or playernum == 8:
        roles = random.choice([["Red", "Red", "Red", "Blue", "Blue", "Blue"],
                               ["Red", "Red", "Blue", "Blue", "Green", "Green"]])
    if playernum == 7:
        roles = ["Red", "Red", "Red", "Blue", "Blue", "Blue", "Green"]
    if playernum == 8:
        roles.append("Red")
        roles.append("Blue")

    random.shuffle(roles)
    roles = dict(enumerate(roles))

    return roles


def chardraw(playernum: int) -> dict:
    fullsetchar = {"Buta-kun1", "Maru-chan1", "Kenya-boi1", "Morimori1", "Fuku-nyan1",
                   "Buta-kun2", "Maru-chan2", "Kenya-boi2", "Morimori2", "Fuku-nyan2",
                   "Buta-kun3", "Maru-chan3", "Kenya-boi3", "Morimori3", "Fuku-nyan3"}

    playerchar = {}

    for i in range(playernum):
        pickset = random.sample(fullsetchar, 3)     # Pick 3 characters for players to select
        for x in pickset:
            fullsetchar.remove(x)       # Remove picked characters from set

        while True:
            charchoice = input("Please select character '1', '2', or '3':\n" + "- ".join(pickset))
            if charchoice in ["1", "2", "3"]:
                break
        playerchar[i] = pickset[int(charchoice) - 1]

    return playerchar


def deckstart() -> dict:

    random.shuffle(maindeck)
    discardpile = []
    fulldeck = {"MainDeck": maindeck, "DiscardPile": discardpile}

    return fulldeck

