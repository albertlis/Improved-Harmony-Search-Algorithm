from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        toolbar = NavigationToolbar(self.canvas, self)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(toolbar)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()
        self.setLayout(vertical_layout)

    def plotData(self, variables, function, lowBounds, upBounds, minMaxValues, trace):
        assert len(variables) == 2
        assert len(minMaxValues) == 2
        x1T, x2T = self.__makeTraceVectors(trace, variables)
        try:
            x1 = np.linspace(lowBounds[0], upBounds[0], 100)
            x2 = np.linspace(lowBounds[1], upBounds[1], 100)
        except ZeroDivisionError as e:
            print(e)
            return
        X1, X2, Z = self.__makeContourVectors(function, x1, x2)
        self.__makePlot(X1, X2, Z, minMaxValues, variables, x1T, x2T)

    def __makeContourVectors(self, function, x1, x2):
        Z = []
        X1, X2 = np.meshgrid(x2, x1)
        for i in range(100):
            Z.append([])
            for j in range(100):
                Z[i].append(function(x1[i], x2[j]))
        return X1, X2, Z

    def __makePlot(self, X1, X2, Z, minMaxValues, variables, x1T, x2T):
        self.canvas.axes.clear()
        im = self.canvas.axes.imshow(Z, interpolation='bilinear', origin='lower',
                                     extent=(minMaxValues[1][0], minMaxValues[1][1],
                                             minMaxValues[0][0], minMaxValues[0][1]),
                                     aspect='auto')
        im.set_alpha(0.5)
        CS = self.canvas.axes.contour(X1, X2, Z, origin='lower', )
        self.canvas.axes.clabel(CS, inline=1, fontsize=10)
        self.canvas.figure.colorbar(im, orientation='vertical', shrink=0.95)
        self.canvas.axes.plot(x2T, x1T, marker=".", c="k")
        self.canvas.axes.grid(True)
        self.canvas.axes.set_xlabel(variables[1])
        self.canvas.axes.set_ylabel(variables[0])
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def __makeTraceVectors(self, trace, variables):
        x1T = np.empty(len(trace))
        x2T = np.empty(len(trace))
        for i, row in enumerate(trace):
            x1T[i], x2T[i] = row[variables[0]], row[variables[1]]
        return x1T, x2T
