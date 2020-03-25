#!/usr/bin/python3
# import random
from sys import path

from matplotlib import cm
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np
from PyQt5 import QtWidgets
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from ui.mainWin import Ui_MainWin
path.append('/ui')


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()


    def calculateButtonClicked(self):
            # print("something")
            X = np.arange(-5, 5, 0.25)
            Y = np.arange(-5, 5, 0.25)
            X, Y = np.meshgrid(X, Y)
            R = np.sqrt(X ** 2 + Y ** 2)
            Z = np.sin(R)

            self.plotWidget.canvas.axes.clear()
            self.plotWidget.canvas.axes.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=1, antialiased=False)
            # self.plotWidget.canvas.axes.set_zlim(-2.01, 2.01)
            # self.plotWidget.canvas.axes.zaxis.set_major_locator(LinearLocator(10))
            # self.plotWidget.canvas.axes.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            self.plotWidget.canvas.draw()

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
