import StartDistribution
import DrawCard
import Database
import PlayerTurn
from datetime import datetime
import pytz
import pandas as pd
import random

"""Database"""

starttime = datetime.now(pytz.timezone('Japan')).strftime("%Y%m%d%H%M%S")
GameDatabase = Database.create_connection(starttime)
Database.startusertable(GameDatabase)

"""Game Preparation"""


# DeckFull = ["Burn1", "Burn2", "Burn 3", "Burn 4",
#            "Burn1", "Burn2", "Burn 3", "Burn 4",
#            "Burn1", "Burn2", "Burn 3", "Burn 4",
#            "Burn1", "Burn2", "Burn 3", "Burn 4",
#            "Burn1", "Burn2", "Burn 3", "Burn 4"
#            ]

DeckFull = StartDistribution.deckstart()
PlayerNum = 5
PlayerRoles = StartDistribution.startrole(PlayerNum)
PlayerChars = StartDistribution.chardraw(PlayerNum)
PlayerHandAll = {}
PlayerMsgAll = {}
for playerid in range(PlayerNum):
    PlayerName = input("Player name?")
    PlayerHandAll[playerid] = []
    DrawCard.draw(DeckFull, PlayerHandAll[playerid], 4)

    PlayerMsgAll[playerid] = []

    Database.createuser(GameDatabase, PlayerName, PlayerChars[playerid], PlayerRoles[playerid])

print(PlayerRoles)
print(PlayerChars)
print(PlayerHandAll)

# Read sqlite query results into a pandas DataFrame
PlayersDF = pd.read_sql_query("SELECT * from users", GameDatabase)

# Verify that result of SQL query is stored in the dataframe
print(PlayersDF.head())

TurnPlayerID = random.choice(range(PlayerNum))

"""Main loop"""
while True:

    """Turn loop"""
    TurnPlayerName = PlayersDF.iloc[TurnPlayerID]["name"]
    input(f"It is now {TurnPlayerName}'s turn. OK?")

    """Draw Phase"""
    PlayerTurn.startturn(DeckFull, TurnPlayerID, PlayerHandAll)

    """Main Phase"""
    PlayerTurn.mainphase(turnplayerid=TurnPlayerID, allhand=PlayerHandAll)

    """Message Phase"""
    PlayerTurn.messagephase(turnplayerid=TurnPlayerID, playerno=PlayerNum, allhand=PlayerHandAll, allmsg=PlayerMsgAll)

    """End Phase"""
    null, discards = PlayerTurn.endphase(turnplayerid=TurnPlayerID, allhand=PlayerHandAll)
    DeckFull, discards = DrawCard.discard(DeckFull, discards)

    """Go to next Player"""
    TurnPlayerID = (TurnPlayerID + 1) % PlayerNum
    print(PlayerHandAll)
