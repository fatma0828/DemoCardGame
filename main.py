import StartDistribution
import DrawCard
import Database
import PlayerTurn
import pandas as pd
import random
from icecream import ic
import pygame
from pygame.locals import QUIT


pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Just Window")
clock = pygame.time.Clock()

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
                                deck=DeckFull,
                                allhand=Database.PlayerHandsDF(),
                                survivor=survivor,
                                allbuffs=PlayerBuffs
                                )

        """End Phase"""
        checkresults = PlayerTurn.endphase(turnplayerid=TurnPlayerID,
                                           deck=DeckFull,
                                           )

        teamwins = checkresults["teamwins"]
        retires = checkresults["retires"]

        surviveDF = PlayersDF()[PlayersDF()['Status'] == 'Alive']
        surviveTeam = surviveDF['role'].unique()

        if retires:
            for player in retires:
                print(f"{PlayerNames[player]} retired.")
                Database.retire(player)
                print(f"{PlayerNames[player]}'s role was {PlayerRoles[player]}")
                DrawCard.discard(DeckFull, PlayerHandAll[player])
                DrawCard.discard(DeckFull, PlayerMsgAll[player])

            if len(surviveDF) == 1:
                winners = [surviveDF['name']]
            ic(surviveTeam)
            print(f"There are {len(surviveTeam)} teams alive!")
            if len(surviveTeam) == 1:
                if "Green" not in surviveTeam:
                    teamwins = surviveTeam

        for player_id in surviveDF.index:
            PlayerBuffs[player_id] = []

        if teamwins:
            winners = [row_index for row_index, (key, value) in enumerate(PlayerRoles.items()) if value in teamwins]

    else:
        print(f"{TurnPlayerName} had retired. Skipping turn.")

    """Go to next Player"""
    TurnPlayerID = (TurnPlayerID + 1) % PlayerNum

    """PYGAME"""
    pygame.display.update()
    clock.tick(1)

for winner in winners:
    status = PlayersDF().iloc[winner]["Status"]
    print(f"{PlayerNames[winner]} ({status}) - {PlayerRoles[winner]} won.")
