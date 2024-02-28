import DrawCard
import GameConditions
import Database
from icecream import ic
import cardtable


playernames = {}
playerroles = {}


def getplayernames(names: dict):
    global playernames
    playernames = names


def getplayerroles(df):
    global playerroles
    playerroles = df['role'].to_dict()


def startturn(deck: dict, turnplayerid: int):

    DrawCard.draw(deck=deck, drawnum=2, playerid=turnplayerid)

    return


def usecardKP(deck: dict):
    allhand = Database.PlayerHandsDF()
    for player_id, hand in allhand.items():
        if any(item.startswith("KP") for item in hand):
            while True:
                usecard = input(f"Does {playernames[player_id]} want to use COUNTER? Input to use, or type 'skip'."
                                f"\n Hand: {hand[player_id]}")
                if usecard in hand and usecard.startswith("KP"):
                    DrawCard.useeffectcard(usecard, deck)
                    return False
                if usecard == "skip":
                    break

    return True


def usecardSJ(turnplayerid: int, usecard: str, survivor: list, deck: dict, allbuffs: dict):
    if usecard.startswith("SJ"):    # 照準の処理
        otherplayers = survivor
        otherplayers.remove(turnplayerid) if turnplayerid in otherplayers else None
        while True:
            try:
                sjtarget = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
                if int(sjtarget) in otherplayers:
                    sjtarget = int(sjtarget)
                    print(f"{playernames[turnplayerid]} is using SJ against {playernames[sjtarget]}.")
                    """ COUNTER-CARD """
                    cardsuccess = usecardKP(deck)
                    if cardsuccess:
                        allbuffs[sjtarget].append("SJ")
                        DrawCard.useeffectcard(usecard, deck)
                    if not cardsuccess:
                        DrawCard.returndeckhand(usecard, deck)
                    break
                if sjtarget == "skip":
                    break
            except ValueError as e:
                print(f"Invalid target. {e}")
    return


def mainphase(turnplayerid: int, allbuffs: dict, deck: dict, survivor: list):
    print(f"Turn player {playernames[turnplayerid]}, You may use cards. Type 'skip' to skip.")
    while True:
        usecard = input(f"Hand: {Database.PlayerHandsDF()[turnplayerid]}, or 'skip'.")
        if usecard in Database.PlayerHandsDF()[turnplayerid]:
            usetime = cardtable.deckcsv.loc[cardtable.deckcsv['CardID'] == usecard, 'Useable'].iloc[0]
            if "MAIN" in usetime:
                print(f"Attempting to use {usecard}.")
                if usecard.startswith("SJ"):    # 照準の処理
                    usecardSJ(turnplayerid, usecard, survivor, deck, allbuffs)
        if usecard == "skip":
            break


def messagephase(turnplayerid: int, playerno: int, allhand: dict,
                 survivor: list, allbuffs: dict):
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

    Database.consumehand(sendmsg)
    ic(survivor)
    rotatingmsg(turnplayerid=turnplayerid, playerno=playerno,
                msgholderid=msgtarget, msgcard=sendmsg,
                survivor=survivor, allbuffs=allbuffs)


# messagephase(0, 5, {0: ["A", "B"], 1: ["A"]}, {0: [], 1: []})

def rotatingmsg(turnplayerid: int, playerno: int, msgholderid: int, msgcard: str,
                survivor: list, allbuffs: dict):

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
            Database.getmsgcard(msgholderid, msgcard)
            print(f"Player {playernames[msgholderid]}'s message zone: {Database.PlayerMsgDF()[msgholderid]}.")
            break

        if msgaccept == "N":
            if msgholderid == turnplayerid or "SJ" in allbuffs[msgholderid]:
                print("You are not allowed to reject.")
                Database.getmsgcard(msgholderid, msgcard)
                print(f"Player {playernames[msgholderid]}'s message zone: {Database.PlayerMsgDF()[msgholderid]}.")
                break

            if ">" in msgcard:
                msgholderid = turnplayerid

            else:
                msgholderid = (msgholderid - 1) % playerno

            print(f"Message rejected. Sent to Player {playernames[msgholderid]}.")


def endphase(turnplayerid: int, deck: dict, allbuffs: dict) -> dict:

    teamwins, retires = GameConditions.teamwincheck(playerroles, Database.PlayerMsgDF())
    checkresults = {"teamwins": teamwins, "retires": retires}
    GameConditions.hand_limit_check(turnplayerid, deck)
    return checkresults

# result, discards = turnendcheck(turnplayerid=1, allhand={0: ["GGG"], 1: ["GGG","GGG","GGG","GGG","GGG","GGG","GGG"]})
