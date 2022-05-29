from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import SelectTournament as st

class AddMatchPage(QDialog):
    def __init__(self):
        super(AddMatchPage, self).__init__()
        self.setWindowTitle("p1")
        loadUi("AddMatchPage.ui", self)
        self.addMatch.clicked.connect(self.addMatchData)
        self.conn = dfl.DataBase()
        self.team_vals = ["Select Team"]
        self.teams = ["Afghanistan", "Australia", "Bangladesh", "England", "India", "New Zealand",
                 "Pakistan", "South Africa", "Sri Lanka", "West indies"]
        self.tournamentData()
        self.t1.addItems(self.team_vals)
        self.t2.addItems(self.team_vals)
        self.hTeam.addItems(self.team_vals)
        
    def tournamentData(self):
        self.conn.cur.execute("SELECT rowid, * FROM Tournament where rowid = " + str(var.tournament))
        df = self.conn.cur.fetchall()[0]
        for team in df[2].split(","):
            self.team_vals.append(self.teams[int(team)-1])
        self.team_indexes = df[2].split(",")
        
    def addMatchData(self):
        team1 = self.t1.currentIndex()
        team2 = self.t2.currentIndex()
        hTeam = self.hTeam.currentIndex()
        m_name = self.mName.text()
        ven = self.venue.text()
        sDate = self.startDate.date().toString("dd-MM-yyyy")
        if(team1 == 0):
            self.warn.setText("Select team 1")
        elif(team2 == 0):
            self.warn.setText("Select team 2")
        elif(hTeam == 0):
            self.warn.setText("Select Home Team")
        elif(m_name == ""):
            self.warn.setText("Enter Match Name")
        elif(ven == ""):
            self.warn.setText("Enter Venue")
        else:
            team1 = int(self.team_indexes[team1-1])
            team2 = int(self.team_indexes[team2-1])
            hTeam = int(self.team_indexes[hTeam-1])
            #self.conn.cur.execute("SELECT id from Matches ORDER BY id DESC LIMIT 1")
            #id_new = int(self.conn.cur.fetchall()[0][0]) + 1
            m_data = [m_name, var.tournament, team1, team2, ven, sDate, hTeam]
            dfl.DataBase().addMatch(m_data)
            self.selTournPage = st.SelectTournamentPage()
            self.selTournPage.show()
            self.close()
        





















