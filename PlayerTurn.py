import DrawCard
import GameConditions


def startturn(deck: dict, turnplayerid: int, allhand: dict):

    turnhand = allhand[turnplayerid]
    DrawCard.draw(deck, turnhand, 2)

    return deck


@GameConditions.handcheck()
def mainphase(turnplayerid: int, allhand: dict):
    print(f"Turn player ID is {turnplayerid}.")
    pass


# mainphase(turnplayerid=1, allhand={"A": 1, "B": "GGG"})

def messagephase(turnplayerid: int, playerno: int, allhand: dict, allmsg: dict):
    print(f"Turn player {turnplayerid}, please send 1 hand card as message.")
    while True:
        sendmsg = input(f"Hand: {allhand[turnplayerid]}")
        if sendmsg in allhand[turnplayerid]:
            break
    if "A" in sendmsg:
        msgtarget = 99
        otherplayers = list(range(playerno))
        otherplayers.remove(turnplayerid)
        while msgtarget not in otherplayers:
            msgtarget = int(input(f"Please select target player ID: {otherplayers}"))
    else:
        msgtarget = (turnplayerid - 1) % playerno

    allhand[turnplayerid].remove(sendmsg)
    rotatingmsg(turnplayerid, playerno, msgtarget, sendmsg, allhand, allmsg)


# messagephase(0, 5, {0: ["A", "B"], 1: ["A"]}, {0: [], 1: []})

def rotatingmsg(turnplayerid: int, playerno: int, msgholderid: int, msgcard: str, allhand: dict, allmsg: dict):
    print(f"{msgcard} is now in front of Player {msgholderid}.")
    """Power Loop"""

    while True:
        msgaccept = input(f"Will {msgholderid} accept the message? Y/N")
        if msgaccept == "Y":
            allmsg[msgholderid].append(msgcard)
            print(f"Player {msgholderid}'s message zone: {allmsg[msgholderid]}.")
            break

        if msgaccept == "N":
            if msgholderid == turnplayerid:
                print("You are not allowed to.")
                allmsg[msgholderid].append(msgcard)
                print(f"Player {msgholderid}'s message zone: {allmsg[msgholderid]}.")
                break

            if "A" in msgcard:
                msgholderid = turnplayerid
            else:
                msgholderid = (msgholderid - 1) % playerno

            print(f"Message rejected. Sent to Player {msgholderid}.")


@GameConditions.turnendcheck()
def endphase(turnplayerid: int, allhand: dict, discards=None):

    return discards

# result, discards = turnendcheck(turnplayerid=1, allhand={0: ["GGG"], 1: ["GGG","GGG","GGG","GGG","GGG","GGG","GGG"]})
