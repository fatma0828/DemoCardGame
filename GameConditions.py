import Database
import DrawCard


# def handcheck(*args, **kwargs):
#    def decorator(func):
#        def wrapper(*args, **kwargs):
#            hand = kwargs.get("allhand", {})
#            turnplayerid = kwargs.get("turnplayerid", {})
#            playerhand = hand[turnplayerid]
#            print(f"Player {turnplayerid}'s hand is {playerhand}.")
#            result = func(*args, **kwargs)
#            return result
#        return wrapper
#    return decorator


def hand_limit_check(turnplayerid: int, deck: dict):
    """Hand Card Limit Check"""
    playerhand = Database.PlayerHandsDF()[turnplayerid]
    print(f"Player {turnplayerid}'s hand is {playerhand}.")

    while len(playerhand) > 6:
        discard = input("Please discard 1 hand.")
        if discard in playerhand:
            DrawCard.discard(deck, [discard])
            playerhand = Database.PlayerHandsDF()[turnplayerid]
            print(f"Player {turnplayerid}'s hand is {playerhand}.")

    return


def teamwincheck(playerroles: dict, msgzone: dict):
    """Team win Check: requires All Msg Zones, All Roles, returns Win Teams"""
    wins = []
    retires = []
    for key, value in playerroles.items():
        if sum(1 for item in msgzone[key] if "x" in item) >= 1:     # 3 Black cards -> retire
            retires.append(key)
        if value == "Red":
            if sum(1 for item in msgzone[key] if "r" in item) >= 1:     # 3 Red cards -> red win
                print(f"There are 3 reds in {msgzone[key]}")
                wins.append("Red")
        if value == "Blue":
            if sum(1 for item in msgzone[key] if "b" in item) >= 1:     # 3 Blue cards -> blue win
                print(f"There are 3 blues in {msgzone[key]}")
                wins.append("Blue")

    return wins, retires
