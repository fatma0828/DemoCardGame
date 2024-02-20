import DrawCard
import GameConditions
import pandas as pd
from icecream import ic

deckcsv = pd.read_csv("deckcards.csv")
maindeck = deckcsv["CardID"].tolist()


def startturn(deck: dict, turnplayerid: int, allhand: dict):

    turnhand = allhand[turnplayerid]
    DrawCard.draw(deck, turnhand, 2)

    return deck


@GameConditions.handcheck()
def mainphase(turnplayerid: int, allhand: dict):
    print(f"Turn player {turnplayerid}, You may use cards. Type 'skip' to skip.")
    while True:
        usecard = input(f"Hand: {allhand[turnplayerid]}")
        if usecard in allhand[turnplayerid]:
            usetime = deckcsv.loc[deckcsv['CardID'] == usecard, 'Useable'].iloc[0]
            if "MAIN" in usetime:
                print(f"Attempting to use {usecard}.")
            break
        if usecard == "skip":
            break


# mainphase(turnplayerid=1, allhand={"A": 1, "B": "GGG"})

def messagephase(turnplayerid: int, playerno: int, allhand: dict, allmsg: dict, survivor: list):
    print(f"Turn player {turnplayerid}, please send 1 hand card as message.")
    while True:
        sendmsg = input(f"Hand: {allhand[turnplayerid]}")
        if sendmsg in allhand[turnplayerid]:
            break
    if ">" in sendmsg:
        otherplayers = survivor
        otherplayers.remove(turnplayerid)
        while True:
            try:
                msgtarget = int(input(f"Please select target player ID: {otherplayers}"))
                if msgtarget in otherplayers:
                    break
            except ValueError:
                print("Invalid target.")
    else:
        msgtarget = (turnplayerid - 1) % playerno

    allhand[turnplayerid].remove(sendmsg)
    rotatingmsg(turnplayerid, playerno, msgtarget, sendmsg, allhand, allmsg, survivor)


# messagephase(0, 5, {0: ["A", "B"], 1: ["A"]}, {0: [], 1: []})

def rotatingmsg(turnplayerid: int, playerno: int, msgholderid: int, msgcard: str,
                allhand: dict, allmsg: dict, survivor: list):
    """Power Loop"""

    while True:
        while msgholderid not in survivor:
            print(f"skipping {msgholderid}")
            msgholderid = (msgholderid - 1) % playerno
        print(f"{msgcard} is now in front of Player {msgholderid}.")
        msgaccept = input(f"Will {msgholderid} accept the message? Y/N")
        if msgaccept == "Y":
            allmsg[msgholderid].append(msgcard)
            print(f"Player {msgholderid}'s message zone: {allmsg[msgholderid]}.")
            break

        if msgaccept == "N":
            if msgholderid == turnplayerid:
                print("You are not allowed to reject.")
                allmsg[msgholderid].append(msgcard)
                print(f"Player {msgholderid}'s message zone: {allmsg[msgholderid]}.")
                break

            if "A" in msgcard:
                msgholderid = turnplayerid
            else:
                msgholderid = (msgholderid - 1) % playerno

            print(f"Message rejected. Sent to Player {msgholderid}.")


@GameConditions.teamwincheck()
@GameConditions.handlimitcheck()
def endphase(turnplayerid: int, deck: dict, allhand: dict, playermsgall: dict, playerroles: dict,
             discards=None, teamwins=None, retires=None) -> dict:
    print(f"From PlayerTurn.py: discards = {discards}")
    DrawCard.discard(deck, discards)
    checkresults = {"teamwins": teamwins, "retires": retires}
    ic(teamwins)
    return checkresults

# result, discards = turnendcheck(turnplayerid=1, allhand={0: ["GGG"], 1: ["GGG","GGG","GGG","GGG","GGG","GGG","GGG"]})
