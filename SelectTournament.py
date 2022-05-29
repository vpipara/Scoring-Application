from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import CreateTournament as ct
import AddMatch as am
import LandingPage as lp

class SelectTournamentPage(QDialog):
    def __init__(self):
        super(SelectTournamentPage, self).__init__()
        self.setWindowTitle("p1")
        loadUi("SelectTournamentPage.ui", self)
        self.t_name = []
        #self.submit.clicked.connect(self.addMatchClicked)
        self.conn = dfl.DataBase()
        self.loadTournaments()
        self.tournamentList.addItems(self.t_name)
        self.addMatch.clicked.connect(self.addMatchbtn)
        self.createTournament.clicked.connect(self.createTournamentbtn)
        self.home.clicked.connect(self.landingPage)
        
    def loadTournaments(self):
        df = self.conn.loadTournaments()
        for k in df:
            self.t_name.append(k[1])
        #cursor.execute("SELECT id from Matches ORDER BY id DESC LIMIT 1")
        #x = cursor.fetchall()
    
    def addMatchbtn(self):
        var.tournament = self.tournamentList.currentIndex()+1
        self.addMatchPage = am.AddMatchPage()
        self.addMatchPage.show()
        self.close()
    
    def createTournamentbtn(self):
        self.createTournPage = ct.CreateTournamentPage()
        self.createTournPage.show()
        self.close()
        
    def landingPage(self):
        self.land_page = lp.LandingPage()
        self.land_page.show()
        self.close()
















