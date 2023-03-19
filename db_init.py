import sqlite3


def initialize_db():
    connection = sqlite3.connect("data-dev.sqlite")
    connection.isolation_level = None
    return connection.cursor()


def create_tables(db):
    db.executescript(
        """CREATE TABLE Games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
        );
        
        CREATE TABLE Levels (
        id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE Emojis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emoji TEXT
        );

        CREATE TABLE Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emoji_id INTEGER REFERENCES Emojis
        );

        CREATE TABLE Levels_Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level_id INTEGER REFERENCES Levels,
        user_id INTEGER REFERENCES Users
        );

        CREATE TABLE Levels_Calcs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level_id INTEGER REFERENCES Levels,
        calc_id INTEGER REFERENCES Calcs
        );

        CREATE TABLE Calcs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        multiplier INTEGER,
        multiplicand INTEGER
        );

        CREATE TABLE Answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES Users,
        calc_id INTEGER REFERENCES Calcs,
        right_answer INTEGER,
        datetime INTEGER
        );
        
        CREATE TABLE Points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        answer_id INTEGER REFERENCES Answers,
        game_id INTEGER REFERENCES Games,
        points INTEGER
        );
        """
    )


from urllib.request import urlopen
import json


def fetch_emojis():
    response = urlopen(
        "https://emojihub.yurace.pro/api/all/category/animals%20and%20nature"
    )
    return json.loads(response.read())


def emojis_into_db(data, db):
    for j in data:
        db.execute(
            """INSERT INTO Emojis(emoji)
            VALUES(?)""",
            j["htmlCode"],
        )


def calcs():
    return [
        {2: [2]},
        {3: [2, 3]},
        {4: [2, 3, 4]},
        {5: [2, 3, 4, 5]},
        {6: [2, 3, 4, 5, 6]},
        {7: [2, 3, 4, 5, 6, 7]},
        {8: [2, 3, 4, 5, 6, 7, 8]},
        {9: [2, 3, 4, 5, 6, 7, 8, 9]},
    ]


def insert_calcs(db):
    for dict in calcs():
        for multiplier, number_list in dict.items():
            for multiplicand in number_list:
                db.execute(
                    """INSERT INTO Calcs(multiplier, multiplicand)
                    VALUES(?,?)""",
                    [multiplier, multiplicand],
                )


def insert_levels(db):
    for level in range(1, 11):
        db.execute(
            """INSERT INTO Levels(id)
                    VALUES(?)""",
            [level],
        )


def insert_games(db):
    games_list = ["Tasot", "Seikkailu"]
    for game in games_list:
        db.execute(
            """INSERT INTO Games(name)
                    VALUES(?)""",
            [game],
        )


def levels_calcs(i):
    # 4
    if 1 <= i <= 4:
        return 1
    elif 5 <= i <= 8:
        return 2
    elif 9 <= i <= 12:
        return 3
    elif 13 <= i <= 16:
        return 4
    elif 17 <= i <= 20:
        return 5
    elif 21 <= i <= 24:
        return 6
    # 3
    elif 25 <= i <= 27:
        return 7
    elif 28 <= i <= 30:
        return 8
    elif 31 <= i <= 33:
        return 9
    else:
        return 10


def insert_levels_calcs(db):
    calcs = db.execute(
        """SELECT C.id, C.multiplier, C.multiplicand
        FROM Calcs C
        ORDER BY C.id"""
    ).fetchall()

    i = 1
    for tuple in calcs:
        calc_id = tuple[0]
        level_id = levels_calcs(i)

        db.execute(
            """INSERT INTO Levels_Calcs(level_id, calc_id)
                    VALUES(?,?)""",
            [level_id, calc_id],
        )
        i += 1


def check_levels(db):
    result = db.execute("SELECT COUNT(*) FROM Levels").fetchone()
    if result[0] > 0:
        return False
    else:
        return True


def insert_db_stuff():
    db = initialize_db()
    if check_levels(db):
        emojis_into_db(fetch_emojis(), db)
        insert_calcs(db)
        insert_levels(db)
        insert_games(db)
        insert_levels_calcs(db)


if __name__ == "__main__":
    db = initialize_db()

    # tables
    # create_tables(db)

    # emojis

    # insert stuff
