import sqlite3
from sqlite3 import Error


def create_connection(starttime):
    path = starttime + ".sqlite"

    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query, **kwargs):
    cursor = connection.cursor()
    try:
        cursor.execute(query, kwargs)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def startusertable(connection):
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL DEFAULT 'DummyName',
      char TEXT NOT NULL DEFAULT 'DummyChar',      
      role TEXT CHECK(role IN ('Red','Blue','Green')) NOT NULL DEFAULT 'Green'
    );
    """

    create_hands_table = """
    CREATE TABLE IF NOT EXISTS hands(
      user_id INTEGER NOT NULL,
      [hand] TEXT NOT NULL DEFAULT 'None',
      FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """

    execute_query(connection, create_users_table)
    execute_query(connection, create_hands_table)


def createuser(connection, name, char, role):
    create_users = """
    INSERT INTO
      users (name, char, role)
    VALUES
      (?, ?, ?);
    """

    cursor = connection.cursor()
    try:
        cursor.execute(create_users, (name, char, role))
        connection.commit()
        print("User created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# execute_query(connection, create_users, userinfo=(name, char, role))
