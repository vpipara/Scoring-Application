from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import LandingPage as lp

class CreatePlayerPage(QDialog):
    def __init__(self):
        super(CreatePlayerPage, self).__init__()
        loadUi("EnterPlayerDetailsPage.ui", self)
        self.submit.clicked.connect(self.submitClicked)
        self.pTeam.addItems(var.teams)
        self.conn = dfl.DataBase()
    
    def submitClicked(self):
        p_name = self.pName.text()
        team = self.pTeam.currentIndex() + 1
        bDate = self.bDate.date().toString("dd-MM-yyyy")
        if(self.batr.isChecked()):
            batHand = 0
        else:
            batHand = 1
        if(self.bowlr.isChecked()):
            bowlHand = 0
        else:
            bowlHand = 1
        #self.conn.cur.execute("SELECT id from Players ORDER BY id DESC LIMIT 1")
        #id_new = int(self.conn.cur.fetchall()[0][0]) + 1
        pl_data = [p_name, team, bDate, batHand, bowlHand]
        dfl.DataBase().addPlayer(pl_data)
        self.land_page = lp.LandingPage()
        self.land_page.show()
        self.close()