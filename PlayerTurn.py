import DrawCard
import GameConditions
from icecream import ic
import cardtable


def startturn(deck: dict, turnplayerid: int, allhand: dict):

    turnhand = allhand[turnplayerid]
    DrawCard.draw(deck, turnhand, 2)

    return deck


@GameConditions.handcheck()
def mainphase(turnplayerid: int, playernames: dict, allhand: dict, allbuffs: dict,
              deck: dict, survivor: list):
    print(f"Turn player {playernames[turnplayerid]}, You may use cards. Type 'skip' to skip.")
    while True:
        usecard = input(f"Hand: {allhand[turnplayerid]}, or 'skip'.")
        if usecard in allhand[turnplayerid]:
            usetime = cardtable.deckcsv.loc[cardtable.deckcsv['CardID'] == usecard, 'Useable'].iloc[0]
            if "MAIN" in usetime:
                print(f"Attempting to use {usecard}.")
                if usecard.startswith("SJ"):
                    otherplayers = survivor
                    otherplayers.remove(turnplayerid)
                    while True:
                        try:
                            sjtarget = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
                            if int(sjtarget) in otherplayers:
                                sjtarget = int(sjtarget)
                                print(f"{playernames[turnplayerid]} is using SJ against {playernames[sjtarget]}.")
                                allbuffs[sjtarget].append("SJ")
                                ic(allhand[turnplayerid])
                                ic(usecard)
                                DrawCard.useeffectcard(allhand[turnplayerid], usecard, deck)
                                break
                            if sjtarget == "skip":
                                break
                        except ValueError as e:
                            print(f"Invalid target. {e}")
        if usecard == "skip":
            break


def messagephase(turnplayerid: int, playerno: int, allhand: dict, allmsg: dict,
                 survivor: list, playernames: dict, allbuffs: dict):
    print(f"Turn player {turnplayerid}, please send 1 hand card as message.")
    while True:
        sendmsg = input(f"Hand: {allhand[turnplayerid]}")
        if sendmsg in allhand[turnplayerid]:
            break
    if ">" in sendmsg:
        otherplayers = [player for player in survivor if player != turnplayerid]
        ic(otherplayers)
        ic(survivor)
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
    ic(survivor)
    rotatingmsg(turnplayerid, playerno, msgtarget, sendmsg, allhand, allmsg, survivor, playernames, allbuffs)


# messagephase(0, 5, {0: ["A", "B"], 1: ["A"]}, {0: [], 1: []})

def rotatingmsg(turnplayerid: int, playerno: int, msgholderid: int, msgcard: str,
                allhand: dict, allmsg: dict, survivor: list, playernames: dict, allbuffs: dict):
    """Power Loop"""

    while True:
        ic(survivor)
        while msgholderid not in survivor:
            print(f"skipping {msgholderid}")
            msgholderid = (msgholderid - 1) % playerno
        if ">" in msgcard or "#" in msgcard:
            print(f"A message is now in front of Player {playernames[msgholderid]}.")
        else:
            print(f"A message: {msgcard} is now in front of Player {playernames[msgholderid]}.")
        msgaccept = input(f"Will {msgholderid} accept the message? Y/N")
        if msgaccept == "Y":
            allmsg[msgholderid].append(msgcard)
            print(f"Player {playernames[msgholderid]}'s message zone: {allmsg[msgholderid]}.")
            break

        if msgaccept == "N":
            if msgholderid == turnplayerid or "SJ" in allbuffs[msgholderid]:
                print("You are not allowed to reject.")
                allmsg[msgholderid].append(msgcard)
                print(f"Player {playernames[msgholderid]}'s message zone: {allmsg[msgholderid]}.")
                break

            if ">" in msgcard:
                msgholderid = turnplayerid

            else:
                msgholderid = (msgholderid - 1) % playerno

            print(f"Message rejected. Sent to Player {playernames[msgholderid]}.")


@GameConditions.teamwincheck()
@GameConditions.handlimitcheck()
def endphase(turnplayerid: int, deck: dict, allhand: dict, playermsgall: dict, playerroles: dict, allbuffs: dict,
             discards=None, teamwins=None, retires=None) -> dict:
    print(f"From PlayerTurn.py: discards = {discards}")
    DrawCard.discard(deck, discards)
    checkresults = {"teamwins": teamwins, "retires": retires}
    ic(teamwins)
    return checkresults

# result, discards = turnendcheck(turnplayerid=1, allhand={0: ["GGG"], 1: ["GGG","GGG","GGG","GGG","GGG","GGG","GGG"]})
