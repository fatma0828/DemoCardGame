import random
from icecream import ic

import Database


def drawone(deck: dict, playerhand: list, playerid: int) -> list:

    if len(deck["MainDeck"]) == 0:      # When no cards to draw, recycle discard pile
        recycle(deck)

    if len(deck["MainDeck"]) == 0:
        print("No more cards to draw.")     # When no cards even after recycle, no draw
        return playerhand

    drawcard = deck["MainDeck"].pop(0)  # Remove card from deck
    playerhand.append(drawcard)         # Add to hand
    Database.drawcard(playerid, drawcard)
    print("Player drawed 1 card.")

    return playerhand


def draw(deck: dict, playerhand: list, playerid: int, drawnum: int) -> list:

    for _ in range(drawnum):
        playerhand = drawone(deck=deck, playerhand=playerhand, playerid=playerid)

    return playerhand


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


def useeffectcard(hand: list, card: str, deck: dict):

    if card:
        hand.remove(card) if card in hand else None
        discard(deck, [card])

    return hand
