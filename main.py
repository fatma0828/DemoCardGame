import StartDistribution
import DrawCard
import Database
import PlayerTurn
import pandas as pd
import random
from icecream import ic


"""Database"""

GameDatabase = Database.GameDatabase
Database.startusertable()


"""Game Preparation"""

DeckFull = StartDistribution.deckstart()
PlayerNum = 5
Database.getPlayerNum(PlayerNum)
PlayerRoles = StartDistribution.startrole(PlayerNum)
PlayerChars = StartDistribution.chardraw(PlayerNum)
PlayerHandAll, PlayerMsgAll, PlayerNames, PlayerBuffs = {}, {}, {}, {}

for playerid in range(PlayerNum):
    while True:
        UserName: str = input("Player name?")
        if UserName:
            PlayerNames[playerid] = UserName
            break
    PlayerHandAll[playerid], PlayerMsgAll[playerid], PlayerBuffs[playerid] = [], [], []

    Database.createuser(UserName, PlayerChars[playerid], PlayerRoles[playerid])

for playerid in range(PlayerNum):
    DrawCard.draw(deck=DeckFull, drawnum=4, playerid=playerid)

PlayerTurn.getplayernames(PlayerNames)

print(PlayerRoles)
print(PlayerChars)


def PlayersDF():
    df = pd.read_sql_query("SELECT * from users", GameDatabase)
    return df


PlayerTurn.getplayerroles(PlayersDF())

ic(Database.PlayerHandsDF())   # Verify that result of SQL query is stored in the dataframe
ic(PlayersDF().head())   # Verify that result of SQL query is stored in the dataframe

TurnPlayerID = random.choice(range(PlayerNum))  # Starting Player on Random

"""Main loop"""
winners = []
while not winners:

    """Turn loop"""
    TurnPlayerName = PlayersDF().iloc[TurnPlayerID]["name"]
    if PlayersDF().iloc[TurnPlayerID]["Status"] == "Alive":
        input(f"It is now {TurnPlayerName}'s turn. OK?")

        """Draw Phase"""
        PlayerTurn.startturn(DeckFull,
                             TurnPlayerID
                             )

        """Main Phase"""
        survivor = PlayersDF()[PlayersDF()['Status'] == 'Alive'].index.tolist()
        PlayerTurn.mainphase(turnplayerid=TurnPlayerID,
                             allbuffs=PlayerBuffs,
                             deck=DeckFull,
                             survivor=survivor
                             )

        """Message Phase"""
        survivor = PlayersDF()[PlayersDF()['Status'] == 'Alive'].index.tolist()
        PlayerTurn.messagephase(turnplayerid=TurnPlayerID,
                                playerno=PlayerNum,
                                allhand=Database.PlayerHandsDF(),
                                survivor=survivor,
                                allbuffs=PlayerBuffs
                                )

        """End Phase"""
        checkresults = PlayerTurn.endphase(turnplayerid=TurnPlayerID,
                                           deck=DeckFull,
                                           allbuffs=PlayerBuffs
                                           )

        teamwins = checkresults["teamwins"]
        retires = checkresults["retires"]

        if retires:
            for player in retires:
                print(f"{PlayerNames[player]} retired.")
                Database.retire(player)
                print(f"{PlayerNames[player]}'s role was {PlayerRoles[player]}")
                DrawCard.discard(DeckFull, PlayerHandAll[player])
                DrawCard.discard(DeckFull, PlayerMsgAll[player])

            surviveDF = PlayersDF()[PlayersDF()['Status'] == 'Alive']
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

for winner in winners:
    status = PlayersDF().iloc[winner]["Status"]
    print(f"{PlayerNames[winner]} ({status}) - {PlayerRoles[winner]} won.")
