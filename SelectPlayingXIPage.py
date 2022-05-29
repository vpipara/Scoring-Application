from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var

class SelectPlayingXIPage(QDialog):
    def __init__(self):
        super(SelectPlayingXIPage, self).__init__()
        loadUi("SelectPlayingXIPage.ui", self)
        self.conn = dfl.DataBase().data
        self.playerList = []
        self.plLabel = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8,
                        self.p9, self.p10, self.p11]
        self.plId = []
        self.codedValue = ""
        cur = self.conn.cursor()
        cur.execute("Select coded from Matches where rowid = " + str(var.match))
        self.coded = cur.fetchall()[0][0]
        if(self.coded == 1):
            self.teamInd = var.t1
        elif(self.coded == 2):
            self.teamInd = var.t2
        self.tName.setText("Add Playing XI of " + var.teams[self.teamInd-1])
        self.getPlayers()
        self.finalXI = []
        self.finalXIname = []
        self.addPlayer.clicked.connect(self.addPlayerClicked)
        self.remPlayer.clicked.connect(self.remPlayerClicked)
        self.submit.clicked.connect(self.submitClicked)
        self.btnDisability()
        
    def getPlayers(self):
        cur = self.conn.cursor()
        cur.execute("Select rowid, * from Players where team = " + str(self.teamInd))
        data = cur.fetchall()
        for i in data:
            self.playerList.append(i[1])
            self.plId.append(i[0])
        self.selPlayer.addItems(self.playerList)
    
    def btnDisability(self):
        if(len(self.finalXI) <= 0):
            self.remPlayer.setEnabled(False)
            self.addPlayer.setEnabled(True)
        if((len(self.finalXI) < 11) & (len(self.finalXI) > 0)):
            self.addPlayer.setEnabled(True)
            self.remPlayer.setEnabled(True)
        if(len(self.finalXI) >= 11):
            self.addPlayer.setEnabled(False)
            self.remPlayer.setEnabled(True)
    
    def addPlayerClicked(self):
        index = self.selPlayer.currentIndex()
        self.finalXI.append(self.plId[index])
        self.finalXIname.append(self.playerList[index])
        self.updateList()
        self.btnDisability()
    
    def remPlayerClicked(self):
        self.finalXI.pop()
        self.finalXIname.pop()
        self.updateList()
        self.btnDisability()
        
    def updateList(self):
        for i in range(len(self.finalXI)):
            self.plLabel[i].setText(self.finalXIname[i])
        for i in range(len(self.finalXI), 11):
            self.plLabel[i].setText("P" + str(i+1))
    
    def submitClicked(self):
        if(self.teamInd == var.t1):
            t = 1
            dfl.DataBase().updateXI(t, self.finalXI)
            self.sameWin = SelectPlayingXIPage()
            self.sameWin.show()
            self.close()
        else:
            t = 2
            dfl.DataBase().updateXI(t, self.finalXI)
            