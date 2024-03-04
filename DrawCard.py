import random
from icecream import ic

import Database


def drawone(deck: dict, playerid: int):

    if len(deck["MainDeck"]) == 0:      # When no cards to draw, recycle discard pile
        recycle(deck)

    if len(deck["MainDeck"]) == 0:
        print("No more cards to draw.")     # When no cards even after recycle, no draw
        return

    drawcard = deck["MainDeck"].pop(0)  # Remove card from deck
    #   playerhand.append(drawcard)
    Database.drawcard(playerid, drawcard)
    print("Player drawed 1 card.")

    return


def draw(deck: dict, playerid: int, drawnum: int):

    for _ in range(drawnum):
        drawone(deck=deck, playerid=playerid)

    return


def recycle(deck: dict) -> dict:
    maindeck = deck["MainDeck"]
    discardpile = deck["DiscardPile"]
    random.shuffle(discardpile) if discardpile else None
    for _ in range(len(discardpile)):
        maindeck.append(discardpile.pop(0))
    print("Discard pile added to main deck.")
    newdeck = {"MainDeck": maindeck, "DiscardPile": discardpile}
    return newdeck


# hand = []
#  = draw(["a", "b", "3", "d", "e", "f"], hand, 3)
# print(hand)

def discard(deck: dict, discards: list):

    if discards:
        for _ in range(len(discards)):
            deck["DiscardPile"].append(discards.pop(0))

    return deck, discards


def useeffectcard(card: str, deck: dict):

    if card:
        Database.consumehand(card)
        discard(deck, [card])

    return


def returndeckhand(card: str, deck: dict):

    if card:
        Database.consumehand(card)
        deck["MainDeck"].append(card)
        ic(deck["MainDeck"][5:])

    return


def returndeckmsg(card: str, deck: dict):

    if card:
        Database.burnmsg(card)
        deck["MainDeck"].append(card)
        ic(deck["MainDeck"][:5])

    return

