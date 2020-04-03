from PyQt5.QtWidgets import QDoubleSpinBox, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

from ui.bandwidthDialog import Ui_bandwidthDialog
from pprint import pprint
from I_IHS import I_IHSAlgorithm


class bandwidthDialog(Ui_bandwidthDialog):
    def __init__(self):
        super(bandwidthDialog, self).__init__()

    def setupUi(self, bwDialog, variables):
        super().setupUi(bwDialog)
        self.__setLayout(bwDialog, variables)
        self.calculateButton.clicked.connect(self.__calculateButtonClicked)

    def __setLayout(self, bwDialog, variables):
        self.variables = variables
        verticalLayout = QVBoxLayout()
        self.__minBoxes = []
        self.__maxBoxes = []
        for var in variables:
            verticalLayout.addLayout(self.__addLineWithBandwidthParameters(var))
        self.calculateButton = self.__makeCalculateButton()
        verticalLayout.addWidget(self.calculateButton)
        bwDialog.setLayout(verticalLayout)

    def __makeCalculateButton(self):
        calculateButton = QPushButton()
        calculateButton.setText("Calculate")
        calculateButton.setObjectName("calculateButton")
        return calculateButton

    def __addLineWithBandwidthParameters(self, var):
        horizontalLayout = QHBoxLayout()
        minText = QLabel(var + ' min:')
        maxText = QLabel('max:')
        minBox = QDoubleSpinBox()
        self.__minBoxes.append(minBox)
        maxBox = QDoubleSpinBox()
        self.__maxBoxes.append(maxBox)
        horizontalLayout.addWidget(minText)
        horizontalLayout.addWidget(minBox)
        horizontalLayout.addWidget(maxText)
        horizontalLayout.addWidget(maxBox)
        return horizontalLayout

    def __calculateButtonClicked(self):
        print('click')
        mins = [minBox.value() for minBox in self.__minBoxes]
        maxes = [maxBox.value() for maxBox in self.__maxBoxes]
        self.__minMaxValues = tuple(zip(mins, maxes))
        pprint(self.__minMaxValues)
        #self.close()


    def getMinMaxValues(self):
        return self.__minMaxValues
"""
    def __calculateButtonClicked(self):
        ihs = I_IHSAlgorithm(self.__readBandwidth())
        ihs.doYourTask()
        print(ihs._f)
        pprint(ihs._HM)
        print(self.__variables)"""
