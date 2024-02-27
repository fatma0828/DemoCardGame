import sqlite3
from sqlite3 import Error
from datetime import datetime
import pytz


def create_connection(starttime):
    path = starttime + ".sqlite"

    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


now = datetime.now(pytz.timezone('Japan')).strftime("%Y%m%d%H%M%S")
GameDatabase = create_connection(now)


def execute_query(query, *args, **kwargs):
    logmsg = kwargs.get("logmsg", None)
    cursor = GameDatabase.cursor()
    try:
        cursor.execute(query, args if args else tuple(kwargs.values()))
        GameDatabase.commit()
        if logmsg:
            print(logmsg)
    except Error as e:
        print(f"The error '{e}' occurred")


def startusertable():
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      userid INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL DEFAULT 'DummyName',
      char TEXT NOT NULL DEFAULT 'DummyChar',      
      role TEXT CHECK(role IN ('Red','Blue','Green')) NOT NULL DEFAULT 'Green',
      [buff] TEXT,
      [Status] TEXT  NOT NULL DEFAULT 'Alive'
    );
    """

    create_cards_table = """
    CREATE TABLE IF NOT EXISTS cards(
      cardid INTEGER PRIMARY KEY AUTOINCREMENT,
      [code] TEXT NOT NULL DEFAULT 'DummyCode',
      [name] TEXT NOT NULL DEFAULT 'DummyCard',
      [user_hand] INTEGER,
      [user_msg] INTEGER,
      FOREIGN KEY (user_hand) REFERENCES users (userid),
      FOREIGN KEY (user_msg) REFERENCES users (userid)
    );
    """

    execute_query(create_users_table)
    execute_query(create_cards_table)


def createuser(name, char, role):
    create_users = """
    INSERT INTO
      users (name, char, role)
    VALUES
      (?, ?, ?);
    """

    execute_query(create_users, name=name, char=char, role=role)

# execute_query(connection, create_users, userinfo=(name, char, role))


def createdeck(code, name):
    insert_card = """
    INSERT INTO
      cards (code, name)
    VALUES
      (?, ?);
    """

    execute_query(insert_card, code, name)


def drawcard(playerid, cardcode):
    update_drawcard = """
    UPDATE cards
    SET user_hand = ?
    WHERE code = ?;
    """

    execute_query(update_drawcard, playerid=playerid, cardcode=cardcode)


def retire(playerid):
    update_retire = """
    UPDATE users
    SET Status = ?
    WHERE userid = ?;
    """

    execute_query(update_retire, "Retire", playerid)
