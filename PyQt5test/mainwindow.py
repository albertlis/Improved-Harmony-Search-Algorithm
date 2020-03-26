from hs import HS
from ui.mainWin import Ui_MainWin


class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()

    def makePlot(self):
        self.plotWidget.plotData()

    def readParameters(self):
        fun = self.functionBox.text()
        iterations = self.iterationsBox.value()
        hms = self.hmsBox.value()
        hmcr = self.hcmrBox.value()
        par = self.parBox.value()
        b = self.bBox.value()
        return fun, iterations, hms, hmcr, par, b

    def calculateButtonClicked(self):
        self.makePlot()
        hs = HS(self.readParameters())

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.calculateButton.clicked.connect(self.calculateButtonClicked)
