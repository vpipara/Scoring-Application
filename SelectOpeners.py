from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var

class SelectOpeners(QDialog):
    def __init__(self):
        super(SelectOpeners, self).__init__()
        loadUi("SelectOpenersWindow.ui", self)
        self.show()
        self.tName.setText("Select openers of " + var.teams[var.batTeam - 1])
        self.cur = dfl.DataBase().cur
        self.loadPlayers()
        self.opener1.addItems(self.players)
        self.opener2.addItems(self.players)
        self.done.clicked.connect(self.doneClicked)
        self.exec_()
    
    def loadPlayers(self):
        self.cur.execute("Select rowid, * from matches where rowid = " + str(var.match))
        match_data = self.cur.fetchall()[0]
        coded_val = match_data[13]
        bat1 = match_data[16]
        t1 = match_data[3]
        if(coded_val == 3):
            if(t1 == bat1):
                self.playersId = match_data[14].split(",")
            else:
                self.playersId = match_data[15].split(",")
        elif(coded_val == 4):
            if(t1 == bat1):
                self.playersId = match_data[15].split(",")
            else:
                self.playersId = match_data[14].split(",")
        self.players = []
        for k in self.playersId:
            self.cur.execute("Select name from Players where rowid = " + str(k))
            self.players.append(self.cur.fetchall()[0][0])

    
    def doneClicked(self):
        var.striker = int(self.playersId[self.opener1.currentIndex()])
        var.nonStriker = int(self.playersId[self.opener2.currentIndex()])
        self.close()