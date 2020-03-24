#!/usr/bin/python3
from sys import path
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from ui.mainWin import Ui_MainWin

path.append('/ui')


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()

    def calculateButtonClicked(self):
        print("Clicked")

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.calculateButton.clicked.connect(self.calculateButtonClicked)

import sys

app = QtWidgets.QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())
