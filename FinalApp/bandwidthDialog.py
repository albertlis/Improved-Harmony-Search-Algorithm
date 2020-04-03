from PyQt5.QtWidgets import QDoubleSpinBox, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel

from ui.bandwidthDialog import Ui_bandwidthDialog
from pprint import pprint
from I_IHS import I_IHSAlgorithm


class bandwidthDialog(Ui_bandwidthDialog):
    def __init__(self):
        super(bandwidthDialog, self).__init__()

    def setupUi(self, bwDialog, variables):
        super().setupUi(bwDialog)
        self.__setLayout(bwDialog, variables)
        # self.calculateButton.clicked.connect(self.__calculateButtonClicked)

    def __setLayout(self, bwDialog, variables):
        verticalLayout = QVBoxLayout()
        for var in variables:
            horizontalLayout = QHBoxLayout()
            minText = QLabel(var + ' min:')
            maxText = QLabel('max:')
            minBox = QDoubleSpinBox()
            maxBox = QDoubleSpinBox()
            horizontalLayout.addWidget(minText)
            horizontalLayout.addWidget(minBox)
            horizontalLayout.addWidget(maxText)
            horizontalLayout.addWidget(maxBox)
            verticalLayout.addLayout(horizontalLayout)
        bwDialog.setLayout(verticalLayout)

"""
    def __calculateButtonClicked(self):
        ihs = I_IHSAlgorithm(self.__readBandwidth())
        ihs.doYourTask()
        print(ihs._f)
        pprint(ihs._HM)
        print(self.__variables)"""
