from pprint import pprint

from PyQt5 import QtWidgets

from I_IHS import I_IHSAlgorithm
from ui.mainWin import Ui_MainWin

from ui.bandwidthDialog import Ui_bandwidthDialog
from bandwidthDialog import bandwidthDialog


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()

    def __makePlot(self):
        self.plotWidget.plotData()

    def __readParameters(self):
        fun = self.functionBox.text()
        iterations = self.iterationsBox.value()
        hms = self.hmsBox.value()
        hmcrMin = self.hcmrMinBox.value()
        hcmrMax = self.hcmrMaxBox.value()
        parMin = self.parMinBox.value()
        parMax = self.parMaxBox.value()
        return fun, iterations, hms, hmcrMin, hcmrMax, parMin, parMax

    def __nextButtonClicked(self):
        mainParameters = self.__readParameters()
        self.__makePlot()
        ihs = I_IHSAlgorithm(mainParameters)

        bwDialog = QtWidgets.QDialog()
        ui = bandwidthDialog()
        ui.setupUi(bwDialog, ihs.getVariables())
        # ui.addVariables(ihs.getVariables())
        bwDialog.exec()
        ihs.doYourTask()

        print(ihs._f)
        pprint(ihs._HM)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.functionBox.setText("2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")
        self.nextButton.clicked.connect(self.__nextButtonClicked)


