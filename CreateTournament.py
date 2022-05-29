from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import SelectTournament as st

class CreateTournamentPage(QDialog):
    def __init__(self):
        super(CreateTournamentPage, self).__init__()
        loadUi("CreateTournamentPage.ui", self)
        self.createBtn.clicked.connect(self.createTmt)
        self.conn = dfl.DataBase()
        
    def createTmt(self):
        team_boxes = [self.afg, self.aus, self.ban, self.eng, self.ind, self.nz, self.pak, self.sa,
                      self.sl, self.wi]
        index = 1
        isChecked = []
        for box in team_boxes:
            if(box.isChecked()):
                isChecked.append(index)
            index += 1
        t_name = self.tName.text()
        sDate = self.startDate.date().toString("dd-MM-yyyy")
        eDate = self.endDate.date().toString("dd-MM-yyyy")
        maxOvers = self.maxOvers.text()
        if(t_name == ""):
            self.warn.setText("Enter tournament name")
        elif(len(isChecked) < 2):
            self.warn.setText("Select at least 2 teams")
        elif(maxOvers == ""):
            self.warn.setText("Enter number of overs")
        else:    
            maxOvers = int(maxOvers)
            #self.conn.cur.execute("SELECT id from Tournament ORDER BY id DESC LIMIT 1")
            #id_new = int(self.conn.cur.fetchall()[0][0]) + 1
            tData = [t_name, isChecked, sDate, eDate, maxOvers]
            dfl.DataBase().addTournament(tData)
            self.selTournPage = st.SelectTournamentPage()
            self.selTournPage.show()
            self.close()
        