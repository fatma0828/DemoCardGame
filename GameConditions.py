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


def turnendcheck(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
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

            # Call the decorated function and pass discards along with other arguments
            result = func(*args, discards=discards, **kwargs)
            return result, discards  # Return the result and the list of discards
        return wrapper
    return decorator
