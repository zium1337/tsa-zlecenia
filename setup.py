import sqlite3

baza = sqlite3.connect("baza.db")


def check():
    try:
        if baza:
            db = baza
            conn = baza.cursor()
            conn.execute("""CREATE TABLE IF NOT EXISTS zlecenia (nick text, czas date)""")
            return db, conn
    except:
        return "Something's wrong!"
