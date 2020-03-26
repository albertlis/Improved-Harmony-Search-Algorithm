#!/usr/bin/python3
import random
from sys import path
from PyQt5 import QtWidgets
import sys

from mainwindow import MainWindow

path.append('/ui')

app = QtWidgets.QApplication(sys.argv)
with open("style.css", "r") as style:
    app.setStyleSheet(style.read())
mainWindow = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())
