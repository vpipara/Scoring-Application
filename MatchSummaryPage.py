from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import pandas as pd
import SelectOpeners as so
import SelectBowler as sb
import ScoreUpdateWindow as su
import SelectBatsmanWindow as sbw

class MatchSummaryPage(QDialog):
    def __init__(self):
        super(MatchSummaryPage, self).__init__()
        loadUi("MatchSummaryWindow.ui", self)
        self.scoreBtn.clicked.connect(self.scoreBtnClicked)
        self.cur = dfl.DataBase().cur
        self.cur.execute("Select rowid, * from Matches where rowid = " + str(var.match))
        self.match_details = self.cur.fetchall()[0]
        self.cur.execute("Select rowid, * from Tournament where rowid = " + str(var.tournament))
        self.tourn_det = self.cur.fetchall()[0]
        self.maxOvers = int(self.tourn_det[-1])
        self.t1Name.setText(var.teams[int(self.match_details[16])-1])
        self.t2Name.setText(var.teams[int(self.match_details[17])-1])
        self.cur.execute("Select rowid, * from BallData where matchId = " + str(var.match))
        self.all_balls = self.cur.fetchall()
        self.all_balls = pd.DataFrame(self.all_balls)
        self.changeSides.clicked.connect(self.changeEnds)
        var.batTeamPlayers = []
        var.bowlTeamPlayers = []
        self.changeInn = 0
        self.getBatBallTeam()
        
    def getBatBallTeam(self):
        coded = self.match_details[13]
        if(coded == 3):
            var.batTeam = int(self.match_details[16])
            var.bowlTeam = int(self.match_details[17])
            if(var.t1 == var.batTeam):
                var.playerIdBat = self.match_details[14].split(",")
                var.playerIdBowl = self.match_details[15].split(",")
            else:
                var.playerIdBat = self.match_details[15].split(",")
                var.playerIdBowl = self.match_details[14].split(",")
            
            var.batTeamPlayers = self.getPlayerNames(var.playerIdBat)
            var.bowlTeamPlayers = self.getPlayerNames(var.playerIdBowl)
            
            if(len(self.all_balls) == 0):
                self.scoreT1.setText("0/0")
                self.oversT1.setText("0.0")
                self.scoreT2.setText("-/-")
                self.oversT2.setText("-")
                self.openers = so.SelectOpeners()
                self.setStrikerDetails(var.striker)
                self.setNonStrikerDetails(var.nonStriker)
                self.bowlerWin = sb.SelectBowler()
                self.setBowlerDetails(var.bowler)
                self.setAllDefault()
            else:
                self.score = self.all_balls[4].sum()
                self.score += self.all_balls[5].sum()
                self.score += self.all_balls[6].sum()
                self.score += self.all_balls[7].sum()
                self.score += self.all_balls[8].sum()
                self.wickets = self.all_balls[14].sum()
                self.scoreT1.setText(str(self.score) + "/" + str(self.wickets))
                self.lastRow = self.all_balls.iloc[-1]
                self.oversT1.setText(str(self.lastRow[9]) + "." + str(self.lastRow[10]))
                var.striker = self.lastRow[2]
                var.nonStriker = self.lastRow[3]
                var.bowler = self.lastRow[11]
                var.over = self.lastRow[9]
                var.ball = self.lastRow[10]
                var.wicket = self.lastRow[14]
                var.playerDismissed = self.lastRow[17]
                var.runs = self.lastRow[8]
                var.legbye = self.lastRow[6]
                var.noball = self.lastRow[5]
                var.wide = self.lastRow[4]
                var.bye = self.lastRow[7]
                self.updateWicket()
                self.updateScores()
                self.updateOver()
                
        elif(coded == 4):
            var.batTeam = int(self.match_details[17])
            var.bowlTeam = int(self.match_details[16])
            
            if(var.t1 == var.batTeam):
                var.playerIdBat = self.match_details[14].split(",")
                var.playerIdBowl = self.match_details[15].split(",")
            else:
                var.playerIdBat = self.match_details[15].split(",")
                var.playerIdBowl = self.match_details[14].split(",")
            
            var.batTeamPlayers = self.getPlayerNames(var.playerIdBat)
            var.bowlTeamPlayers = self.getPlayerNames(var.playerIdBowl)
            
            self.loadFirstInning()
            second_inning = self.all_balls[self.all_balls[12] == var.batTeam]
            if(len(second_inning) == 0):
                self.scoreT2.setText("0/0")
                self.oversT2.setText("0.0")
                self.selectOpeners = so.SelectOpeners()
                self.selectBowler = sb.SelectBowler()
                self.setStrikerDetails(var.striker)
                self.setNonStrikerDetails(var.nonStriker)
                self.setBowlerDetails(var.bowler)
                self.setAllDefault()
            else:
                last_ball = second_inning.iloc[-1]
                self.updateScoreCard()
                var.striker = last_ball[2]
                var.nonStriker = last_ball[3]
                var.bowler = last_ball[11]
                var.over = last_ball[9]
                var.ball = last_ball[10]
                var.wicket = last_ball[14]
                var.playerDismissed = last_ball[17]
                var.runs = last_ball[8]
                var.legbye = last_ball[6]
                var.noball = last_ball[5]
                var.wide = last_ball[4]
                var.bye = last_ball[7]
                self.updateWicket()
                self.updateScores()
                self.updateOver()
        else:
            print("completed")
    
    def getPlayerNames(self, playerId):
        names = []
        for k in playerId:
            self.cur.execute("Select name from Players where rowid = " + str(k))
            names.append(self.cur.fetchall()[0][0])
        return names
    
    def findPlayerName(self, index, playerId, playerNames):
        k = 0
        for k in range(len(playerId)):
            if(int(playerId[k]) == index):
                return playerNames[k]
            k += 1
    
    def getBatsmanData(self, player_id):
        if(len(self.all_balls) == 0):
            data = ["-", "-", "-", "-", "-"]
        else:
            player_balls = self.all_balls[self.all_balls[2] == player_id]
            if(len(player_balls) == 0):
                data = ["-", "-", "-", "-", "-"]
            else:
                runs = player_balls[8].sum()
                balls = len(player_balls[player_balls[4] == 0])
                fours = len(player_balls[player_balls[8] == 4])
                sixes = len(player_balls[player_balls[8] == 6])
                sr = round(runs/balls, 2)*100
                if(balls == 0):
                    data = ["-", "-", "-", "-", "-"]
                else:
                    data = [runs, balls, fours, sixes, sr]
        return data
    
    def getBowlerData(self, player_id):
        if(len(self.all_balls) == 0):
            data = ["-", "-", "-", "-", "-"]
        else:
            player_balls = self.all_balls[self.all_balls[11] == player_id]
            if(len(player_balls) == 0):
                data = ["-", "-", "-", "-", "-"]
            else:
                runs = player_balls[8].sum()
                runs += player_balls[4].sum()
                runs += player_balls[5].sum()
                balls = len(player_balls[(player_balls[4] == 0) & (player_balls[5] == 0)])
                overs = str(int(balls/6))
                overs += "." + str(balls%6)
                #print(overs)
                dots = len(player_balls[((player_balls[4] == 0) & (player_balls[5] == 0)) & (player_balls[8] == 0)])
                wickets = len(player_balls[(player_balls[14] == 1) & (player_balls[15] != 5)])
                extras = player_balls[4].sum()
                extras += player_balls[5].sum()
                if(balls == 0):
                    data = ["-", "-", "-", "-", "-"]
                else:
                    data = [overs, dots, runs, wickets, extras]
        return data
    
    def setAllDefault(self):
        var.runs = 0
        var.over = 0
        var.ball = 0
        var.wide = 0
        var.noball = 0
        var.legbye = 0
        var.bye = 0
        var.wicket = 0
        var.wicket_type = 0
        var.fielder = 0
        var.playerDismissed = 0
    
    def scoreBtnClicked(self):
        self.scoreWindow = su.ScoreUpdateWindow()
        self.cur.execute("Select rowid, * from BallData where matchId = " + str(var.match))
        self.all_balls = self.cur.fetchall()
        self.all_balls = pd.DataFrame(self.all_balls)
        self.updateScoreCard()
        self.checkInningsEnd()
        if(self.changeInn == 0):
            self.updateWicket()
            self.updateScores()
            self.updateOver()
        self.changeInn = 0
    
    def updateWicket(self):
        if(var.wicket == 1):
            self.newBatsman = sbw.SelectBatsman()
            if(var.playerDismissed == var.striker):
                var.striker = var.newPlayer
            else:
                var.nonStriker = var.newPlayer
        var.newPlayer = 0
        self.setStrikerDetails(var.striker)
        self.setNonStrikerDetails(var.nonStriker)

    def updateOver(self):
        if(var.ball == 6):
            if((var.wide == 0) & (var.noball == 0)):
                self.bowlerWin = sb.SelectBowler()
                self.changeEnds()
                var.over += 1
        self.setBowlerDetails(var.bowler)
            
    
    def changeEnds(self):
        strik = var.striker
        var.striker = var.nonStriker
        var.nonStriker = strik
        self.setStrikerDetails(var.striker)
        self.setNonStrikerDetails(var.nonStriker)
    
    def updateScores(self):
        if(((var.runs%2 != 0) | (var.bye%2 != 0)) | (var.legbye%2 != 0)):
            self.changeEnds()
        if((var.wide>0) & (var.wide%2 == 0)):
            self.changeEnds()
        
    def setStrikerDetails(self, striker):
        sData = self.getBatsmanData(striker)
        self.striker.setText(self.findPlayerName(striker, var.playerIdBat, var.batTeamPlayers))
        self.sRuns.setText(str(sData[0]))
        self.sBalls.setText(str(sData[1]))
        self.sFours.setText(str(sData[2]))
        self.sSixes.setText(str(sData[3]))
        self.sSR.setText(str(sData[4]))
    
    def setNonStrikerDetails(self, striker):
        nsData = self.getBatsmanData(striker)
        self.nonStriker.setText(self.findPlayerName(striker, var.playerIdBat, var.batTeamPlayers))
        self.nsRuns.setText(str(nsData[0]))
        self.nsBalls.setText(str(nsData[1]))
        self.nsFours.setText(str(nsData[2]))
        self.nsSixes.setText(str(nsData[3]))
        self.nsSR.setText(str(nsData[4]))
    
    def setBowlerDetails(self, bowler):
        bData = self.getBowlerData(bowler)
        self.bowler.setText(self.findPlayerName(var.bowler, var.playerIdBowl, var.bowlTeamPlayers))
        self.bOvers.setText(str(bData[0]))
        self.bDots.setText(str(bData[1]))
        self.bRuns.setText(str(bData[2]))
        self.bWickets.setText(str(bData[3]))
        self.bExtras.setText(str(bData[4]))
    
    def updateScoreCard(self):
        team_balls = self.all_balls[self.all_balls[12] == var.batTeam]
        self.score = team_balls[4].sum()
        self.score += team_balls[5].sum()
        self.score += team_balls[6].sum()
        self.score += team_balls[7].sum()
        self.score += team_balls[8].sum()
        self.wickets = team_balls[14].sum()
        over = team_balls.iloc[-1][9]
        ball = team_balls.iloc[-1][10]
        if(self.match_details[13] == 3):
            self.scoreT1.setText(str(self.score) + "/" + str(self.wickets))
            self.oversT1.setText(str(over) + "." + str(ball))
        else:
            self.scoreT2.setText(str(self.score) + "/" + str(self.wickets))
            self.oversT2.setText(str(over) + "." + str(ball))
        
    def checkInningsEnd(self):
        if(((var.over == self.maxOvers-1) & (var.ball == 6)) | (self.wickets == 10)):
            if(self.match_details[13] == 3):
                self.changeInn = 1
                conn = dfl.DataBase().data
                cur = conn.cursor()
                cur.execute("update Matches set coded = 4 where rowid = " + str(var.match))
                conn.commit()
                temp = var.batTeam
                var.batTeam = var.bowlTeam
                var.bowlTeam = temp
                self.setAllDefault()
                temp = var.batTeamPlayers
                var.batTeamPlayers = var.bowlTeamPlayers
                var.bowlTeamPlayers = temp
                temp = var.playerIdBat
                var.playerIdBat = var.playerIdBowl
                var.playerIdBowl = temp
                self.loadFirstInning()
                self.scoreT2.setText("0/0")
                self.oversT2.setText("0.0")
                self.selectOpeners = so.SelectOpeners()
                self.selectBowler = sb.SelectBowler()
                self.setStrikerDetails(var.striker)
                self.setNonStrikerDetails(var.nonStriker)
                self.setBowlerDetails(var.bowler)
                self.setAllDefault()
                self.cur.execute("Select rowid, * from Matches where rowid = " + str(var.match))
                self.match_details = self.cur.fetchall()[0]
            else:
                self.changeInn = 1
                conn = dfl.DataBase().data
                cur = conn.cursor()
                cur.execute("update Matches set coded = 5 where rowid = " + str(var.match))
                if(self.score >= self.target):
                    cur.execute("update Matches set winner = " + str(var.batTeam) + " where rowid = " + str(var.match))
                    conn.commit()
                    cur.execute("update Matches set margin_wickets = " + str(10-self.wickets) + " where rowid = " + str(var.match))
                    conn.commit()
                    self.close()
                else:
                    cur.execute("update Matches set winner = " + str(var.bowlTeam) + " where rowid = " + str(var.match))
                    conn.commit()
                    cur.execute("update Matches set margin_runs = " + str((self.target - self.score) - 1) + " where rowid = " + str(var.match))
                    conn.commit()
                    self.close()
        if(self.match_details[13] == 4):
            conn = dfl.DataBase().data
            cur = conn.cursor()
            print(self.target - self.score)
            if(self.score >= self.target):
                self.changeInn = 1
                cur.execute("update Matches set winner = " + str(var.batTeam) + " where rowid = " + str(var.match))
                conn.commit()
                cur.execute("update Matches set margin_wickets = " + str(10-self.wickets) + " where rowid = " + str(var.match))
                conn.commit()
                cur.execute("update Matches set coded = 5 where rowid = " + str(var.match))
                conn.commit()
                self.close()
    
    def loadFirstInning(self):
        #print(var.bowlTeam)
        team_balls = self.all_balls[self.all_balls[12] == var.bowlTeam]
        self.score = team_balls[4].sum()
        self.score += team_balls[5].sum()
        self.score += team_balls[6].sum()
        self.score += team_balls[7].sum()
        self.score += team_balls[8].sum()
        self.wickets = team_balls[14].sum()
        self.scoreT1.setText(str(self.score) + "/" + str(self.wickets))
        #print(team_balls)
        over = team_balls.iloc[-1][9]
        ball = team_balls.iloc[-1][10]
        self.oversT1.setText(str(over) + "." + str(ball))
        self.target = self.score+1  
            


























