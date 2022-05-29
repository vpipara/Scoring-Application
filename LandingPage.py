from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import SelectTournament as st
import SelectMatchPage as smp
import EnterPlayerDetailsPage as epd
import App_code as ac

class LandingPage(QDialog):
    def __init__(self):
        super(LandingPage, self).__init__()
        self.setWindowTitle("p1")
        loadUi("LandingPage.ui", self)
        self.addMatch.clicked.connect(self.addMatchClicked)
        self.scoreMatch.clicked.connect(self.scoreMatchClicked)
        self.addPlayers.clicked.connect(self.addPlayerClicked)
        self.signOut.clicked.connect(self.signOutClicked)
        var.tournament = ""
        var.match = ""
    
    def addMatchClicked(self):
        self.selTournPage = st.SelectTournamentPage()
        self.selTournPage.show()
        self.close()
    
    def scoreMatchClicked(self):
        self.selMatchPg = smp.SelectMatchPage()
        self.selMatchPg.show()
        self.close()
    
    def addPlayerClicked(self):
        self.createPlPg = epd.CreatePlayerPage()
        self.createPlPg.show()
        self.close()
        
    def signOutClicked(self):
        self.loginPage = ac.HomePage()
        self.loginPage.show()
        self.close()