from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import SelectPlayingXIPage as spxi

class TossDetailsPage(QDialog):
    def __init__(self):
        super(TossDetailsPage, self).__init__()
        loadUi("TossDetailsPage.ui", self)
        self.t1.setText(var.teams[var.t1 - 1])
        self.t2.setText(var.teams[var.t2 - 1])
        self.playingXI.clicked.connect(self.playingXIClicked)
        print(var.match)
    
    def getBatTeam(self):
        if(self.t1.isChecked()):
            if(self.bat.isChecked()):
                var.batTeam = var.t1
                var.bowlTeam = var.t2
            else:
                var.batTeam = var.t2
                var.bowlTeam = var.t1
        else:
            if(self.bat.isChecked()):
                var.batTeam = var.t2
                var.bowlTeam = var.t1
            else:
                var.batTeam = var.t1
                var.bowlTeam = var.t2
                
    def playingXIClicked(self):
        self.getBatTeam()
        if(self.t1.isChecked()):
            toss_winner = var.t1
        else:
            toss_winner = var.t2
        if(self.bat.isChecked()):
            dec = 0
        else:
            dec = 1
        dfl.DataBase().updateToss(toss_winner, dec)
        self.playxiPage = spxi.SelectPlayingXIPage()
        self.playxiPage.show()
        self.close()