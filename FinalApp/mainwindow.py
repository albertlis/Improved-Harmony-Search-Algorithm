from pprint import pprint

from I_IHS import I_IHSAlgorithm
from ui.mainWin import Ui_MainWin
from BandwidthDialog import BandwidthDialog


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
        ihs = I_IHSAlgorithm(mainParameters)

        ui = BandwidthDialog()
        ui.setupUi(ihs.getVariables())
        ui.exec()
        minMaxBandwidthValues = ui.getMinMaxValues()
        #zmodyfikowac aby wszystkie przekazac
        # ihs.setBW(minMaxBandwidthValues[0])
        ihs.doYourTask()
        self.__makePlot()

        print(ihs._f)
        pprint(ihs._HM)

    def __hcmrMaxValueChanged(self):
        if self.hcmrMaxBox.value() <= self.hcmrMinBox.value():
            self.hcmrMinBox.setValue(self.hcmrMaxBox.value() - 0.2)

    def __hcmrMinValueChanged(self):
        if self.hcmrMaxBox.value() <= self.hcmrMinBox.value():
            self.hcmrMaxBox.setValue(self.hcmrMaxBox.value() + 0.2)

    def __parMinValueChanged(self):
        if self.parMaxBox.value() <= self.parMinBox.value():
            self.parMaxBox.setValue(self.parMinBox.value() + 0.2)

    def __parMaxValueChanged(self):
        if self.parMaxBox.value() <= self.parMinBox.value():
            self.parMinBox.setValue(self.parMaxBox.value() - 0.2)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.functionBox.setText("2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")
        self.nextButton.clicked.connect(self.__nextButtonClicked)
        self.hcmrMaxBox.valueChanged.connect(self.__hcmrMaxValueChanged)
        self.hcmrMinBox.valueChanged.connect(self.__hcmrMinValueChanged)
        self.parMaxBox.valueChanged.connect(self.__parMaxValueChanged)
        self.parMinBox.valueChanged.connect(self.__parMinValueChanged)


