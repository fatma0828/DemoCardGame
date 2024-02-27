def handcheck(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            hand = kwargs.get("allhand", None)
            turnplayerid = kwargs.get("turnplayerid", None)
            playerhand = hand[turnplayerid]
            print(f"Player {turnplayerid}'s hand is {playerhand}.")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def handlimitcheck(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            """Hand Card Limit Check"""
            hand = kwargs.get("allhand", None)
            turnplayerid = kwargs.get("turnplayerid", None)
            playerhand = hand.get(turnplayerid, [])
            print(f"Player {turnplayerid}'s hand is {playerhand}.")

            discards = []  # List to store discards
            while len(playerhand) > 6:
                discard = input("Please discard 1 hand.")
                if discard in playerhand:
                    playerhand.remove(discard)
                    discards.append(discard)  # Add discard to the list
                    print(f"Player {turnplayerid}'s hand is {playerhand}.")

            result = func(*args, discards=discards, **kwargs)
            return result
        return wrapper
    return decorator


def teamwincheck(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            """Team win Check: requires All Msg Zones, All Roles, returns Win Teams"""
            wins = []
            retires = []
            msgzone = kwargs.get("playermsgall", None)
            playerroles = kwargs.get("playerroles", None)
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

            result = func(*args, teamwins=wins, retires=retires, **kwargs)
            return result
        return wrapper
    return decorator
