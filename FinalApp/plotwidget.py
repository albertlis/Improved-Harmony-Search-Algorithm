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
        self._cbar = None

    def plotData(self, variables, function, lowBounds, upBounds, minMaxValues, trace):
        if len(variables) == 2 and len(minMaxValues) == 2:
            x1T, x2T = self.__makeTraceVectors(trace, variables)
            try:
                x1 = np.linspace(lowBounds[0], upBounds[0], 200)
                x2 = np.linspace(lowBounds[1], upBounds[1], 200)
            except ZeroDivisionError as e:
                # print(e)
                return
            Z, min, max = self.__makeContourVectors(function, x1, x2)
            self.__makePlot(Z, minMaxValues, variables, x1T, x2T, min, max)

    def __makeContourVectors(self, function, x1, x2):
        x1Len = len(x1)
        x2Len = len(x2)
        Z = np.empty(shape=(x1Len, x2Len))
        min = 10000000
        max = -10000000
        for i in range(x1Len):
            for j in range(x2Len):
                val = function(x1[i], x2[j])
                Z[i][j] = val
                if val < min:
                    min = val
                if val > max:
                    max = val
        return Z, min, max

    def __makePlot(self, Z, minMaxValues, variables, x1T, x2T, min, max):
        self.canvas.axes.clear()
        im = self.canvas.axes.imshow(Z, interpolation='bilinear', origin='lower',
                                     extent=(minMaxValues[1][0], minMaxValues[1][1],
                                             minMaxValues[0][0], minMaxValues[0][1]),
                                     aspect='auto')
        im.set_alpha(0.5)
        levels1 = np.linspace(min, max/1000., num=10)
        levels2 = np.linspace(max/1000., max/2, num=15)
        levels2 = np.append(levels2, max)
        levels = np.concatenate((levels1, levels2[1:]))
        levels = np.sort(levels)
        CS = self.canvas.axes.contour(Z, levels, origin='lower', linewidths=1,
                                      extent=(minMaxValues[1][0], minMaxValues[1][1],
                                              minMaxValues[0][0], minMaxValues[0][1]))
        self.canvas.axes.clabel(CS, inline=1, fontsize=10)
        if self._cbar is None:
            self._cbar = self.canvas.figure.colorbar(im, orientation='vertical', shrink=0.95)
        else:
            self._cbar.remove()
            self._cbar = self.canvas.figure.colorbar(im, orientation='vertical', shrink=0.95)
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
