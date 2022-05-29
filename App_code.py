from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi
import data_file as dfl
import variables as var
import AddMatch as am
import LandingPage as lp

class HomePage(QDialog):
    def __init__(self):
        super(HomePage, self).__init__()
        self.setWindowTitle("p1")
        loadUi("HomePage.ui", self)
        self.login.clicked.connect(self.checkCred)
        self.forgotPass.clicked.connect(self.showPass)
        self.conn = dfl.DataBase()

    def checkCred(self):
        username = self.username.text()
        password = self.password.text()
        self.warning.setStyleSheet("color: red")
        if(username == ""):
            self.warning.setText("Enter Username")
        elif(password == ""):
            self.warning.setText("Enter Password")
        else:
            originalPass = self.conn.checkPassword(username)
            if(originalPass == "NOT FOUND"):
                self.warning.setText("Enter valid username")
            else:
                if(originalPass == password):
                    self.warning.setText("Login Successful")
                    self.warning.setStyleSheet("color: green")
                    var.user = username
                    self.land_page = lp.LandingPage()
                    self.land_page.show()
                    self.close()
                else:
                    self.warning.setText("Incorrect Password")
        
    def showPass(self):
        username = self.username.text()
        if(username == ""):
            self.warning.setText("Enter Username")
        else:
            originalPass = self.conn.checkPassword(username)
            if(originalPass == "NOT FOUND"):
                self.warning.setText("Enter valid username")
            else:
                self.warning.setText("The password is : " + originalPass)
                self.warning.setStyleSheet("color: green")

"""app = QApplication(sys.argv)
win = HomePage()
win.show()
try:
    sys.exit(app.exec_())
except:
    pass"""