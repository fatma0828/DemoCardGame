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
PlayerRoles = StartDistribution.startrole(PlayerNum)
PlayerChars = StartDistribution.chardraw(PlayerNum)
PlayerHandAll = {}
PlayerMsgAll = {}
PlayerNames = {}
PlayerBuffs = {}

for playerid in range(PlayerNum):
    while True:
        UserName: str = input("Player name?")
        if UserName:
            PlayerNames[playerid] = UserName
            break
    PlayerHandAll[playerid] = []

    PlayerMsgAll[playerid] = []
    PlayerBuffs[playerid] = []

    Database.createuser(UserName, PlayerChars[playerid], PlayerRoles[playerid])

for playerid in range(PlayerNum):
    DrawCard.draw(deck=DeckFull, playerhand=PlayerHandAll[playerid], drawnum=4, playerid=playerid)

print(PlayerRoles)
print(PlayerChars)
ic(PlayerHandAll)


# Read sqlite query results into a pandas DataFrame
def PlayersDF():
    df = pd.read_sql_query("SELECT * from users", GameDatabase)
    return df


def PlayerHandsDF():
    # SQL query to fetch data
    query = f"""
        SELECT user_hand, code
        FROM cards
        WHERE user_hand IN ({','.join('?' for _ in range(PlayerNum))});
    """

    # Parameters for the SQL query (range(PlayerNum))
    params = list(range(PlayerNum))

    # Execute the query and fetch data into a DataFrame
    df = pd.read_sql_query(query, GameDatabase, params=params)

    # Group by user_hand and aggregate the codes into lists
    grouped = df.groupby('user_hand')['code'].agg(list)

    # Convert the grouped DataFrame to a dictionary
    user_hands_dict = grouped.to_dict()

    return user_hands_dict


ic(PlayerHandsDF())   # Verify that result of SQL query is stored in the dataframe
ic(PlayerHandAll == PlayerHandsDF())
print(PlayersDF().head())   # Verify that result of SQL query is stored in the dataframe

TurnPlayerID = random.choice(range(PlayerNum))  # Starting Player on Random

"""Main loop"""
winners = []
while not winners:

    """Turn loop"""
    TurnPlayerName = PlayersDF().iloc[TurnPlayerID]["name"]
    if PlayersDF().iloc[TurnPlayerID]["Status"] == "Alive":
        input(f"It is now {TurnPlayerName}'s turn. OK?")

        """Draw Phase"""
        PlayerTurn.startturn(DeckFull, TurnPlayerID, PlayerHandAll)

        """Main Phase"""
        survivor = PlayersDF()[PlayersDF()['Status'] == 'Alive'].index.tolist()
        PlayerTurn.mainphase(turnplayerid=TurnPlayerID, playernames=PlayerNames,
                             allhand=PlayerHandAll, allbuffs=PlayerBuffs, deck=DeckFull, survivor=survivor)

        """Message Phase"""
        survivor = PlayersDF()[PlayersDF()['Status'] == 'Alive'].index.tolist()
        PlayerTurn.messagephase(turnplayerid=TurnPlayerID, playerno=PlayerNum,
                                allhand=PlayerHandAll, allmsg=PlayerMsgAll,
                                survivor=survivor, playernames=PlayerNames, allbuffs=PlayerBuffs)

        """End Phase"""
        checkresults = PlayerTurn.endphase(turnplayerid=TurnPlayerID, deck=DeckFull, allhand=PlayerHandAll,
                                           playermsgall=PlayerMsgAll, playerroles=PlayerRoles, allbuffs=PlayerBuffs)

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
    print(PlayerHandAll)

for winner in winners:
    status = PlayersDF().iloc[winner]["Status"]
    print(f"{PlayerNames[winner]} ({status}) - {PlayerRoles[winner]} won.")
