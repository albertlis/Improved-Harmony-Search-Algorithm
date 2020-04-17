from PyQt5.QtWidgets import *
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from VariablesParser import *


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

    def plotData(self, variables, function, lowBounds, upBounds, minMaxValues):
        assert len(variables) == 2
        assert len(minMaxValues) == 2
        Z = []
        try:
            x1 = np.arange(lowBounds[0], upBounds[0], (upBounds[0] - lowBounds[0]) / 1000)
            x2 = np.arange(lowBounds[1], upBounds[1], (upBounds[0] - lowBounds[0]) / 1000)
        except ZeroDivisionError as e:
            print(e)
            return
        X1, X2 = np.meshgrid(x1, x2)
        for i in range(1000):
            Z.append([])
            for j in range(1000):
                Z[i].append(function(x1[i], x2[j]))

        self.canvas.axes.clear()
        im = self.canvas.axes.imshow(Z, interpolation='bilinear', origin='lower',
                                     extent=(minMaxValues[0][0], minMaxValues[0][1],
                                             minMaxValues[1][0], minMaxValues[1][1]))
        im.set_alpha(0.5)
        CS = self.canvas.axes.contour(X1, X2, Z, origin='lower', )
        self.canvas.axes.clabel(CS, inline=1, fontsize=10)
        self.canvas.figure.colorbar(im, orientation='vertical', shrink=0.95)
        self.canvas.axes.grid(True)
        self.canvas.axes.set_xlabel(variables[0])
        self.canvas.axes.set_ylabel(variables[1])
        self.canvas.figure.tight_layout()
        self.canvas.draw()
