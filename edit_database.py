import sqlite3

data = sqlite3.connect("Database.db")
cur = data.cursor()
cur.execute("Update BallData set matchID = 1605 where matchId = 4")
data.commit()
cur.execute("Update Matches set coded = 3 where rowid = 4")
data.commit()
data.close()