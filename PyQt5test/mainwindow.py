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
        parMin = self.parMinBox.value()
        parMax = self.parMaxBox.value()
        bandwidthMin = self.bandwidthMinBox.value()
        bandwidthMax = self.bandwidthMaxBox.value()
        return fun, iterations, hms, hmcr, parMin, parMax, bandwidthMin, bandwidthMax

    def calculateButtonClicked(self):
        self.makePlot()
        hs = HS(self.readParameters())
        print(hs)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.calculateButton.clicked.connect(self.calculateButtonClicked)
