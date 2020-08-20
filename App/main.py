#!/usr/bin/python3
from sys import path
from PyQt5 import QtWidgets
from resource_path import resource_path
from mainwindow import MainWindow
import sys


path.append('/ui')

app = QtWidgets.QApplication(sys.argv)
with open(resource_path("style.css"), "r") as style:
    app.setStyleSheet(style.read())
mainWindow = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())