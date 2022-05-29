import sqlite3
import variables as var

class DataBase():
    def __init__(self):
        self.data = sqlite3.connect("Database.db")
        self.cur = self.data.cursor()
    
    def closeConnection(self):
        self.data.close()
    
    def createUsersTable(self):
        try:
            self.cur.execute("CREATE TABLE Users ('username' text, 'password' text)")
            self.cur.execute("INSERT INTO Users ('username', 'password') VALUES ('admin', 'Password')")
            self.data.commit()
        except:
            pass
    
    def createTournamentTable(self):
        try:
            self.cur.execute(""" CREATE TABLE Tournament ('tournamentName' text,
                                                          'teams' text, 'startDate' text, 'endDate' text,
                                                          'winner' integer, 'max_overs' integer)""")
            #self.addTournament([0, "test", [1, 2], "01/01/2001", "01/02/2001", 50])
            self.data.commit()
        except:
            pass
    
    def createMatchesTable(self):
        try:
            self.cur.execute("""CREATE TABLE Matches ('matchName' text, 'tournament' integer,
                                                      'Team1' integer,'Team2' integer, 'toss' integer, 'decision' integer,
                                                      'winner' integer, 'margin_runs' integer, 'margin_wickets' integer,
                                                      'venue' text, 'startDate' text, 'homeOf' integer, 'coded' integer,
                                                      't1XI' text, 't2XI' text, 'bat1' integer, 'bat2' integer)""")
            #self.addMatch([0, "test", 0, 1, 2, "test", "01/01/2001", 1])
            self.data.commit()
        except:
            pass
    
    def createPlayersTable(self):
        try:
            self.cur.execute("""CREATE TABLE Players ('name' text, 'team' integer,
                                                      'birthDate' text, 'battingHand' integer,
                                                      'bowlingHand' integer) """)
            #self.addPlayer([0, "Vaibhav Pipara", 5, "16-05-1999", 0, 0])
            self.data.commit()
        except:
            pass
    
    def createBallDataTable(self):
        try:
            self.cur.execute(""" CREATE TABLE BallData ('matchId' integer, 'striker' integer,
                                                        'nonStriker' integer, 'wide' integer,
                                                        'noBall' integer, 'legByes' integer,
                                                        'byes' integer, 'batRuns' integer,
                                                        'over' integer, 'ball' integer, 'bowler' integer,
                                                        'batTeam' integer, 'bowlTeam' integer,
                                                        'wicket' integer, 'wicket_type' integer,
                                                        'fielder' integer, 'playerDismissed' integer)""")
            self.data.commit()
        except:
            pass
    
    def checkPassword(self, username):
        self.cur.execute("SELECT password from Users where username = '" + str(username) + "'")
        df = self.cur.fetchall()
        if(len(df) > 0):
            return df[0][0]
        else:
            return "NOT FOUND"
    
    def addTournament(self, vals):
        final_string = ""
        for i in range(0, 1):
            final_string += "'" + vals[i] + "', "
        team_str = ""
        for i in vals[1]:
            team_str += str(i) + ","
        team_str = team_str[:-1]
        final_string += "'" + team_str + "', "
        for i in range(2, 4):
            final_string += "'" + vals[i] + "', " 
        final_string += str(vals[4]) + ")"
        #final_string = final_string[:-2] + ")"
        self.cur.execute("""INSERT INTO Tournament ('tournamentName', 'teams', 'startDate', 'endDate', 'max_overs') 
                         VALUES (""" + final_string)
        self.data.commit()
    
    def addMatch(self, vals):
        final_string = ""
        for i in range(0, 1):
            final_string += "'" + vals[i] + "', " 
        final_string += str(vals[1]) + ", "
        for i in range(2, 4):
            final_string += str(vals[i]) + ", "
        for i in range(4, 6):
            final_string += "'" + vals[i] + "', " 
        
        final_string += str(vals[6]) + ", 0)"
        self.cur.execute("""INSERT INTO Matches ('matchName', 'tournament', 'team1', 'team2',
                                                 'venue', 'startDate', 'homeOf', 'coded') VALUES (""" + final_string)
        self.data.commit()
    
    def addPlayer(self, vals):
        final_string = ""
        final_string += "'" + vals[0] + "', "
        final_string += str(vals[1]) + ", "
        final_string += "'" + vals[2] + "', "
        final_string += str(vals[3]) + ", "
        final_string += str(vals[4]) + ")"
        self.cur.execute("""INSERT INTO Players ('name', 'team', 'birthDate',
                                                 'battingHand', 'bowlingHand') values (""" + final_string)
        self.data.commit()
    
    def addGameBall(self, vals):
        final_string = ""
        for i in vals:
            final_string += str(i) + ", "
        final_string = final_string[:-2] + ")"
        self.cur.execute(""" INSERT INTO BallData ('matchId', 'striker', 'nonStriker',
                                                   'wide', 'noball', 'legByes', 'byes',
                                                   'batRuns', 'over', 'ball', 'bowler', 'batTeam',
                                                   'bowlTeam', 'wicket', wicket_type, 'fielder',
                                                   'playerDismissed') values (""" + final_string)
        self.data.commit()
    
    def loadTournaments(self):
        self.cur.execute("SELECT rowid, * FROM Tournament")
        df = self.cur.fetchall()
        return df
    
    def updateToss(self, winner, dec):
        self.cur.execute("Update Matches set toss = " + str(winner) + ", decision = " + str(dec) + 
                         ", coded = 1, bat1 = " + str(var.batTeam) + 
                         ", bat2 = " + str(var.bowlTeam) + " where rowid = " + str(var.match))
        self.data.commit()
    
    def updateXI(self, t, vals):
        final_string = ""
        for k in vals:
            final_string += str(k) + ","
        final_string = final_string[:-1]
        if(t == 1):
            self.cur.execute("Update Matches set t1XI = '" + final_string + 
                             "', coded = 2 where rowid = " + str(var.match))
        else:
            self.cur.execute("Update Matches set t2XI = '" + final_string + 
                             "', coded = 3 where rowid = " + str(var.match))
        self.data.commit()


t = DataBase()
t.createUsersTable()
t.createMatchesTable()
t.createTournamentTable()
t.createPlayersTable()
t.createBallDataTable()
#t.closeConnection()