from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import SelectTournament as st
import TossDetailsPage as tdp
import SelectPlayingXIPage as spxi
import MatchSummaryPage as smp

class SelectMatchPage(QDialog):
    def __init__(self):
        super(SelectMatchPage, self).__init__()
        loadUi("SelectMatchPage.ui", self)
        self.conn = dfl.DataBase()
        self.name_tourn = []
        self.name_match = []
        self.loadTournament()
        self.tournament.addItems(self.name_tourn)
        self.matches = []
        self.match.clear()
        self.match.addItems(self.name_match)
        self.tournament.currentIndexChanged.connect(self.tournChange)
        self.loadMatch(1)
        self.start.clicked.connect(self.getM)
        
    def loadTournament(self):
        cur = self.conn.data.cursor()
        cur.execute("SELECT rowid, * from Tournament")
        all_tour = cur.fetchall()
        for i in all_tour:
            self.name_tourn.append(i[1])
            
    def loadMatch(self, tourn):
        cur = self.conn.data.cursor()
        cur.execute("SELECT rowid, * from Matches where tournament = " + str(tourn))# + " and coded = 0")
        self.matches = cur.fetchall()
        self.name_match = []
        for i in self.matches:
            self.name_match.append(i[1])
        self.match.clear()
        self.match.addItems(self.name_match)
    
    def tournChange(self, i):
        var.tournament = i+1
        self.loadMatch(i+1)
        
    def getM(self):
        match_ind = self.match.currentIndex()
        var.match = self.matches[match_ind][0]
        var.t1 = self.matches[match_ind][3]
        var.t2 = self.matches[match_ind][4]
        coded_num = self.matches[match_ind][13]
        if(coded_num == 0):
            self.tossDetPg = tdp.TossDetailsPage()
            self.tossDetPg.show()
            self.close()
        elif(coded_num == 1):
            self.playxiPage = spxi.SelectPlayingXIPage()
            self.playxiPage.show()
            self.close()
        elif(coded_num == 2):
            self.playxiPage = spxi.SelectPlayingXIPage()
            self.playxiPage.show()
            self.close()
        elif(coded_num >= 3):
            self.matchSum = smp.MatchSummaryPage()
            self.matchSum.show()
            self.close()
        
























