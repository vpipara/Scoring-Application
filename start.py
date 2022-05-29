import App_code as ac
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout
import sys
from PyQt5.uic import loadUi

app = QApplication(sys.argv)
win = ac.HomePage()
win.show()
try:
    sys.exit(app.exec_())
except:
    pass