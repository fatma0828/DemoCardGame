import StartDistribution
import DrawCard
import Database
import PlayerTurn
from datetime import datetime
import pytz
import pandas as pd
import random
from icecream import ic


"""Database"""

starttime = datetime.now(pytz.timezone('Japan')).strftime("%Y%m%d%H%M%S")
GameDatabase = Database.create_connection(starttime)
Database.startusertable(GameDatabase)

"""Game Preparation"""

DeckFull = StartDistribution.deckstart()
PlayerNum = 5
PlayerRoles = StartDistribution.startrole(PlayerNum)
PlayerChars = StartDistribution.chardraw(PlayerNum)
PlayerHandAll = {}
PlayerMsgAll = {}
PlayerNames = {}
for playerid in range(PlayerNum):
    while True:
        UserName: str = input("Player name?")
        if UserName:
            PlayerNames[playerid] = UserName
            break
    PlayerHandAll[playerid] = []
    DrawCard.draw(DeckFull, PlayerHandAll[playerid], 4)

    PlayerMsgAll[playerid] = []

    Database.createuser(GameDatabase, UserName, PlayerChars[playerid], PlayerRoles[playerid])

print(PlayerRoles)
print(PlayerChars)
print(PlayerHandAll)

# Read sqlite query results into a pandas DataFrame
PlayersDF = pd.read_sql_query("SELECT * from users", GameDatabase)
PlayersDF["Status"] = "Alive"

# Verify that result of SQL query is stored in the dataframe
print(PlayersDF.head())

TurnPlayerID = random.choice(range(PlayerNum))

"""Main loop"""
winners = []
while not winners:

    """Turn loop"""
    TurnPlayerName = PlayersDF.iloc[TurnPlayerID]["name"]
    if PlayersDF.iloc[TurnPlayerID]["Status"] == "Alive":
        input(f"It is now {TurnPlayerName}'s turn. OK?")

        """Draw Phase"""
        PlayerTurn.startturn(DeckFull, TurnPlayerID, PlayerHandAll)

        """Main Phase"""
        PlayerTurn.mainphase(turnplayerid=TurnPlayerID, allhand=PlayerHandAll)

        """Message Phase"""
        survivor = PlayersDF[PlayersDF['Status'] == 'Alive'].index.tolist()
        PlayerTurn.messagephase(turnplayerid=TurnPlayerID, playerno=PlayerNum,
                                allhand=PlayerHandAll, allmsg=PlayerMsgAll,
                                survivor=survivor)

        """End Phase"""
        checkresults = PlayerTurn.endphase(turnplayerid=TurnPlayerID, deck=DeckFull, allhand=PlayerHandAll,
                                           playermsgall=PlayerMsgAll, playerroles=PlayerRoles)

        teamwins = checkresults["teamwins"]
        retires = checkresults["retires"]

        if retires:
            for player in retires:
                print(f"{PlayerNames[player]} retired.")
                PlayersDF.iloc[player, PlayersDF.columns.get_loc("Status")] = "Retire"
                print(f"{PlayerNames[player]}'s role was {PlayerRoles[player]}")
                DrawCard.discard(DeckFull, PlayerHandAll[player])
                DrawCard.discard(DeckFull, PlayerMsgAll[player])

            surviveDF = PlayersDF[PlayersDF['Status'] == 'Alive']
            if len(surviveDF) == 1:
                winners = [surviveDF['name']]
            surviveTeam = surviveDF['role'].unique()
            ic(surviveTeam)
            print(f"There are {len(surviveTeam)} teams alive!")
            if len(surviveTeam) == 1:
                if "Green" not in surviveTeam:
                    teamwins = surviveTeam

        if teamwins:
            winners = [row_index for row_index, (key, value) in enumerate(PlayerRoles.items()) if value in teamwins]

    else:
        print(f"{TurnPlayerName} had retired. Skipping turn.")

    """Go to next Player"""
    TurnPlayerID = (TurnPlayerID + 1) % PlayerNum
    print(PlayerHandAll)

for winner in winners:
    print(f"{PlayerNames[winner]} - {PlayerRoles[winner]} won.")
