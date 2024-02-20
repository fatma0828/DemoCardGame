import random


def drawone(deck: dict, playerhand: list) -> list:

    if len(deck["MainDeck"]) == 0:      # When no cards to draw, recycle discard pile
        recycle(deck)

    if len(deck["MainDeck"]) == 0:
        print("No more cards to draw.")     # When no cards even after recycle, no draw
        return playerhand

    playerhand.append(deck["MainDeck"].pop(0))      # Remove card from deck
    print("Player drawed 1 card.")

    return playerhand


def draw(deck: dict, playerhand: list, drawnum: int) -> list:

    for _ in range(drawnum):
        playerhand = drawone(deck, playerhand)

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
