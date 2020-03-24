#!/usr/bin/python3
import random
from sys import path
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from PyQt5 import QtWidgets
from ui.mainWin import Ui_MainWin
path.append('/ui')


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()


    def calculateButtonClicked(self):
            # print("something")
            fs = 500
            f = random.randint(1, 100)
            ts = 1 / fs
            length_of_signal = 100
            t = np.linspace(0, 1, length_of_signal)
            cosinus_signal = np.cos(2 * np.pi * f * t)
            sinus_signal = np.sin(2 * np.pi * f * t)

            self.plotWidget.canvas.axes.clear()
            self.plotWidget.canvas.axes.plot(t, cosinus_signal)
            self.plotWidget.canvas.axes.plot(t, sinus_signal)
            self.plotWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
            self.plotWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
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
