from PyQt5.QtWidgets import QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

from ui.bandwidthDialog import Ui_bandwidthDialog
from pprint import pprint


class BandwidthDialog(Ui_bandwidthDialog):
    def __init__(self):
        super(BandwidthDialog, self).__init__()
        self.__minBoxes = []
        self.__maxBoxes = []
        self.__minMaxValues = ()

    def setupUi(self, variables):
        super().setupUi(self)
        self.__setLayout(self, variables)
        self.calculateButton.clicked.connect(self.__calculateButtonClicked)

    def __setLayout(self, bwDialog, variables):
        # self.variables = variables
        verticalLayout = QVBoxLayout()
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
        minValues = [minBox.value() for minBox in self.__minBoxes]
        maxValues = [maxBox.value() for maxBox in self.__maxBoxes]
        self.__minMaxValues = tuple(zip(minValues, maxValues))
        # pprint(self.__minMaxValues)
        self.close()

    def getMinMaxValues(self):
        if not hasattr(self, '__minMaxValues'):
            self.__minMaxValues = ((0.0, 0.0), (0.0, 0.0))
        return self.__minMaxValues
