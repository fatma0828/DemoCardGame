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


def showmsglocation(msgcard: str, msgholderid: int):
    if ">" in msgcard or "#" in msgcard:  # 直達の場合
        print(f"A message is now in front of Player {playernames[msgholderid]}.")
    else:
        print(f"A message: {msgcard} is now in front of Player {playernames[msgholderid]}.")


def startturn(deck: dict, turnplayerid: int):

    DrawCard.draw(deck=deck, drawnum=2, playerid=turnplayerid)

    return


def usecardKP(deck: dict, turnplayerid: int):
    allhand = Database.PlayerHandsDF()

    start_player_id = turnplayerid
    player_ids = list(allhand.keys())
    player_ids_reordered = player_ids[start_player_id:] + player_ids[:start_player_id]

    for player_id in player_ids_reordered:
        hand = allhand[player_id]

        if any(item.startswith("KP") for item in hand):
            while True:
                usecard = input(f"Does {playernames[player_id]} want to use COUNTER? Input to use, or type 'skip'."
                                f"\n Hand: {hand}")
                if usecard in hand and usecard.startswith("KP"):
                    DrawCard.useeffectcard(usecard, deck)
                    return False
                if usecard == "skip":
                    break
    return True


def usecardSJ(turnplayerid: int, usecard: str, survivor: list, deck: dict, allbuffs: dict):
    otherplayers = survivor
    otherplayers.remove(turnplayerid) if turnplayerid in otherplayers else None     # Cannot use on turn player
    while True:
        try:
            sj_target = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
            if int(sj_target) in otherplayers:
                sj_target = int(sj_target)
                print(f"{playernames[turnplayerid]} is using SJ against {playernames[sj_target]}.")
                """ COUNTER-CARD """
                cardsuccess = usecardKP(deck, turnplayerid)
                if cardsuccess:
                    allbuffs[sj_target].append("SJ")
                    DrawCard.useeffectcard(usecard, deck)
                if not cardsuccess:
                    DrawCard.returndeckhand(usecard, deck)
                break
            if sj_target == "skip":
                break
        except ValueError as e:
            print(f"Invalid target. {e}")
    return


def usecardTS(turnplayerid: int, usecard: str, survivor: list, deck: dict):
    otherplayers = survivor
    otherplayers.remove(turnplayerid) if turnplayerid in otherplayers else None     # Cannot use on self
    while True:
        try:
            ts_target = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
            if int(ts_target) in otherplayers:
                ts_target = int(ts_target)
                print(f"{playernames[turnplayerid]} is using 偵察 against {playernames[ts_target]}.")
                """ COUNTER-CARD """
                cardsuccess = usecardKP(deck, turnplayerid)
                if cardsuccess:
                    if "r" in usecard and playerroles[ts_target] != "Red":
                        DrawCard.drawone(deck, ts_target)
                    if "b" in usecard and playerroles[ts_target] != "Blue":
                        DrawCard.drawone(deck, ts_target)
                    if "x" in usecard and playerroles[ts_target] != "Green":
                        DrawCard.drawone(deck, ts_target)
                    DrawCard.useeffectcard(usecard, deck)
                if not cardsuccess:
                    DrawCard.returndeckhand(usecard, deck)
                break
            if ts_target == "skip":
                break
        except ValueError as e:
            print(f"Invalid target. {e}")
    return


def usecardYK(turnplayerid: int, userid: int, usecard: str, deck: dict, allbuffs: dict):
    """ COUNTER-CARD """
    cardsuccess = usecardKP(deck, turnplayerid)
    if cardsuccess:
        allbuffs[turnplayerid].append("YK")     # 横取りの処理
        allbuffs[userid].append("YK")     # 横取りの処理
        DrawCard.useeffectcard(usecard, deck)
        return True
    if not cardsuccess:
        DrawCard.returndeckhand(usecard, deck)
        return False


def usecardOT(turnplayerid: int, msgholderid: int, usecard: str, survivor: list, deck: dict, allbuffs: dict):
    otherplayers = survivor
    otherplayers.remove(turnplayerid) if turnplayerid in otherplayers else None     # Cannot use on turn player
    otherplayers.remove(msgholderid) if msgholderid in otherplayers else None     # Cannot use on self
    while True:
        try:
            ot_target = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
            if int(ot_target) in otherplayers:
                ot_target = int(ot_target)
                print(f"{playernames[turnplayerid]} is using OT against {playernames[ot_target]}.")
                if "SJ" in allbuffs[ot_target]:
                    print(f"{playernames[ot_target]} は照準されていますので、発動できません。")
                    break
                """ COUNTER-CARD """
                cardsuccess = usecardKP(deck, turnplayerid)
                if cardsuccess:
                    allbuffs[ot_target].append("OT")    # 囮作戦の処理
                    DrawCard.useeffectcard(usecard, deck)
                if not cardsuccess:
                    DrawCard.returndeckhand(usecard, deck)
                break
            if ot_target == "skip":
                break
        except ValueError as e:
            print(f"Invalid target. {e}")
    return


def usecardSR(turnplayerid: int, usecard: str, deck: dict):
    """ COUNTER-CARD """
    cardsuccess = usecardKP(deck, turnplayerid)
    if cardsuccess:
        DrawCard.useeffectcard(usecard, deck)
        return True
    if not cardsuccess:
        DrawCard.returndeckhand(usecard, deck)
        return False


def usecardKT(turnplayerid: int, usecard: str, deck: dict):
    """ COUNTER-CARD """
    cardsuccess = usecardKP(deck, turnplayerid)
    if cardsuccess:
        DrawCard.useeffectcard(usecard, deck)
        return True
    if not cardsuccess:
        DrawCard.returndeckhand(usecard, deck)
        return False


def usecardSK(turnplayerid: int, usecard: str, survivor: list, deck: dict):
    if usecard.startswith("SK"):    # 焼却の処理
        otherplayers = survivor
        while True:
            try:
                sk_target = input(f"Please select target player ID: {otherplayers} or stop by 'skip'.")
                if int(sk_target) in otherplayers:
                    sk_target = int(sk_target)
                    print(f"{playernames[turnplayerid]} is using OT against {playernames[sk_target]}.")
                    """ COUNTER-CARD """
                    cardsuccess = usecardKP(deck, turnplayerid)

                    if cardsuccess:
                        while True:
                            burncard = input(f"Select 1 black card from: {Database.PlayerMsgDF()[sk_target]}")
                            if "x" not in burncard:
                                print("Please select black card only.")
                                continue
                            if burncard in Database.PlayerMsgDF()[sk_target]:
                                DrawCard.returndeckmsg(burncard, deck)

                        DrawCard.useeffectcard(usecard, deck)

                    if not cardsuccess:
                        DrawCard.returndeckhand(usecard, deck)
                    break
                if sk_target == "skip":
                    break
            except ValueError as e:
                print(f"Invalid target. {e}")
    return


def mainphase(turnplayerid: int, allbuffs: dict, deck: dict, survivor: list):
    while True:
        print(f"Turn player {playernames[turnplayerid]}, You may use cards. Type 'skip' to skip.")
        usecard = input(f"Hand: {Database.PlayerHandsDF()[turnplayerid]}, or 'skip'.")
        if usecard in Database.PlayerHandsDF()[turnplayerid]:
            if usecard.startswith("SJ"):    # 照準の処理
                print(f"Attempting to use {usecard}.")
                usecardSJ(turnplayerid, usecard, survivor, deck, allbuffs)
            if usecard.startswith("TS"):    # 偵察の処理
                print(f"Attempting to use {usecard}.")
                usecardTS(turnplayerid, usecard, survivor, deck)
        if usecard == "skip":
            break


def messagephase(turnplayerid: int, playerno: int, allhand: dict, deck: dict,
                 survivor: list, allbuffs: dict):
    print(f"Turn player {playernames[turnplayerid]}, please send 1 hand card as message.")
    while True:
        sendmsg = input(f"Hand: {allhand[turnplayerid]}")
        if sendmsg in allhand[turnplayerid]:
            break
    if ">" in sendmsg:
        otherplayers = [player for player in survivor if player != turnplayerid]
        while True:
            try:
                msgtarget = int(input(f"Please select target player ID: {otherplayers}"))
                if msgtarget in otherplayers:
                    receivers = [msgtarget, turnplayerid]
                    break
            except ValueError:
                print("Invalid target.")
    else:
        receivers = list(range(turnplayerid - 1, -1, -1)) + list(range(playerno - 1, turnplayerid - 1, -1))
        receivers = [player_id for player_id in receivers if player_id in survivor]

    ic(receivers)
    Database.consumehand(sendmsg)
    rotatingmsg(turnplayerid=turnplayerid, deck=deck, msgcard=sendmsg,
                survivor=survivor, allbuffs=allbuffs, receivers=receivers)


# messagephase(0, 5, {0: ["A", "B"], 1: ["A"]}, {0: [], 1: []})

def rotatingmsg(turnplayerid: int, deck: dict, msgcard: str,
                survivor: list, allbuffs: dict, receivers: list):
    msgorder = 0

    while True:
        msgholderid = receivers[msgorder]

        while msgholderid not in survivor:          # 生存確認
            print(f"Skipping retired {playernames[msgholderid]}.")
            msgorder = (msgorder + 1) % len(receivers)
            ic(allbuffs)

        msgholderid = receivers[msgorder]
        ic(receivers)
        showmsglocation(msgcard, msgholderid)

        """CARD TIME: YK, OT, SR (msgholder), KT (msgholder)"""
        player_ids_reordered = survivor[turnplayerid:] + survivor[:turnplayerid]
        for player_id in player_ids_reordered:
            while True:
                allhand = Database.PlayerHandsDF()
                usecard = input(f"Does {playernames[player_id]} want to use cards? Input to use, or type 'skip'."
                                f"\n Hand: {allhand[player_id]}")
                if usecard.startswith("YK"):
                    yk_sucess = usecardYK(turnplayerid, player_id, usecard, deck, allbuffs)
                    if yk_sucess:
                        receivers = [player_id, turnplayerid]     # 横取りの処理
                        msgorder = 0
                        msgholderid = receivers[msgorder]

                    showmsglocation(msgcard, msgholderid)

                if usecard.startswith("OT"):
                    usecardOT(turnplayerid, msgholderid, usecard, survivor, deck, allbuffs)

                if usecard.startswith("SR"):
                    if player_id != msgholderid:
                        print("You are not message holder.")
                        break
                    sr_success = usecardSR(turnplayerid, usecard, deck)
                    if sr_success:
                        deck["MainDeck"].append(msgcard)
                        ic(deck["MainDeck"][:5])
                        msgcard = usecard                           # すり替えの処理

                if usecard.startswith("KT"):
                    if player_id != msgholderid:
                        print("You are not message holder.")
                        break
                    kt_success = usecardSR(turnplayerid, usecard, deck)
                    if kt_success:
                        print(f"The message is {usecard}.")

                if usecard == "skip":
                    break

        while True:
            msgaccept = input(f"Will {playernames[msgholderid]} accept the message? Y/N")
            if msgaccept == "Y" or msgaccept == "N":
                break

        if msgaccept == "Y":
            if "OT" in allbuffs[msgholderid]:
                msgaccept = "N"
            else:
                Database.getmsgcard(msgholderid, msgcard)
                print(f"Player {playernames[msgholderid]}'s message zone: {Database.PlayerMsgDF()[msgholderid]}.")
                usecardSK(turnplayerid, usecard, survivor, deck)
                break

        if msgaccept == "N":
            if msgholderid == turnplayerid or "SJ" in allbuffs[msgholderid]:
                print("You are not allowed to reject.")
                Database.getmsgcard(msgholderid, msgcard)
                print(f"Player {playernames[msgholderid]}'s message zone: {Database.PlayerMsgDF()[msgholderid]}.")
                usecardSK(turnplayerid, usecard, survivor, deck)
                break

            else:
                msgorder = (msgorder + 1) % len(receivers)
                msgholderid = receivers[msgorder]
                ic(receivers)

                print(f"Message rejected. Sent to Player {playernames[msgholderid]}.")


def endphase(turnplayerid: int, deck: dict) -> dict:

    teamwins, retires = GameConditions.teamwincheck(playerroles, Database.PlayerMsgDF())
    checkresults = {"teamwins": teamwins, "retires": retires}
    GameConditions.hand_limit_check(turnplayerid, deck)
    return checkresults

# result, discards = turnendcheck(turnplayerid=1, allhand={0: ["GGG"], 1: ["GGG","GGG","GGG","GGG","GGG","GGG","GGG"]})
