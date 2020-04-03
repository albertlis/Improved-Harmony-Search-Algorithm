from I_IHS import I_IHSAlgorithm
from ui.mainWin import Ui_MainWin
from pprint import pprint


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()

    def makePlot(self):
        self.plotWidget.plotData()

    def readParameters(self):
        fun = self.functionBox.text()
        iterations = self.iterationsBox.value()
        hms = self.hmsBox.value()
        hmcrMin = self.hcmrMinBox.value()
        hcmrMax = self.hcmrMaxBox.value()
        parMin = self.parMinBox.value()
        parMax = self.parMaxBox.value()
        return fun, iterations, hms, hmcrMin, hcmrMax, parMin, parMax

    def calculateButtonClicked(self):
        self.makePlot()
        self.readParameters()
        ihs = I_IHSAlgorithm(self.readParameters())
        ihs.doYourTask()
        print(ihs._f)
        pprint(ihs._HM)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.functionBox.setText("2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")
        self.calculateButton.clicked.connect(self.calculateButtonClicked)
