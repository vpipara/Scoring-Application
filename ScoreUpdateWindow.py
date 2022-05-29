from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var

class ScoreUpdateWindow(QDialog):
    def __init__(self):
        super(ScoreUpdateWindow, self).__init__()
        loadUi("ScoreUpdateWindow.ui", self)
        self.show()
        self.cur = dfl.DataBase().cur
        self.done.clicked.connect(self.doneClicked)
        self.wicketDetails()
        self.wicket.stateChanged.connect(self.wicketDetails)
        self.exec_()

    def wicketDetails(self):
        if(self.wicket.isChecked()):
            self.wicketType.setEnabled(True)
            self.playerDismissed.setEnabled(True)
            self.label.setEnabled(True)
            self.wicketType.clear()
            wicket_types = ["Select Wicket Type", "Caught", "Bowled", "LBW", "Stumped", "Run Out", "Retired Hurt"]
            self.wicketType.addItems(wicket_types)
            self.playerDismissed.clear()
            players = self.getPlayerNames([var.striker, var.nonStriker])
            playersId = [var.striker, var.nonStriker]
            self.playerDismissed.addItems(players)
            var.wicket = 1
            var.wicket_type = self.wicketType.currentIndex()
            var.playerDismissed = playersId[self.playerDismissed.currentIndex()]
        else:
            self.wicketType.setEnabled(False)
            self.playerDismissed.setEnabled(False)
            self.label.setEnabled(False)
            self.wicketType.clear()
            self.playerDismissed.clear()
            var.wicket = 0
            var.wicket_type = 0
            var.playerDismissed = 0
        
    def doneClicked(self):
        var.runs = 0
        #var.ball = 0
        #var.over = 0
        var.wide = 0
        var.noball = 0
        var.legbye = 0
        var.bye = 0
        var.fielder = 0
        if(self.runs0.isChecked()):
            var.runs = 0
        elif(self.runs1.isChecked()):
            var.runs = 1
        elif(self.runs2.isChecked()):
            var.runs = 2
        elif(self.runs3.isChecked()):
            var.runs = 3
        elif(self.runs4.isChecked()):
            var.runs = 4
        elif(self.runs5.isChecked()):
            var.runs = 5
        elif(self.runs6.isChecked()):
            var.runs = 6
        if(self.wide.isChecked()):
            var.wide = 1 + var.runs
            var.runs = 0
        if(self.noball.isChecked()):
            var.noball = 1
        if(self.bye.isChecked()):
            var.bye = var.runs
            var.runs = 0
        if(self.legbye.isChecked()):
            var.legbye = var.runs
            var.runs = 0
        if((var.wide == 0) & (var.noball == 0)):
            if(var.ball == 6):
                var.ball = 1
            else:
                var.ball += 1
        vals = [var.match, var.striker, var.nonStriker, var.wide, var.noball, var.legbye,
                var.bye, var.runs, var.over, var.ball, var.bowler, var.batTeam, var.bowlTeam,
                var.wicket, var.wicket_type, var.fielder, var.playerDismissed]
        dfl.DataBase().addGameBall(vals)
        self.close()
        
    def getPlayerNames(self, playerId):
        names = []
        for k in playerId:
            self.cur.execute("Select name from Players where rowid = " + str(k))
            names.append(self.cur.fetchall()[0][0])
        return names