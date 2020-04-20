from pprint import pprint

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect

from FunctionChooseDialog import FunctionChooseDialog
from I_IHS import I_IHSAlgorithm
from ui.mainWin import Ui_MainWin
from BandwidthDialog import BandwidthDialog
from VariablesParser import *
from PyQt5 import QtCore

class MainWindow(Ui_MainWin):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.boxesValueOffset = 0.000001
        self.__minMaxBandwidthValues = (0, 0)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.functionBox.setPlaceholderText("np. pow(x1,2)+log(xyx, e)")
        self.__connectSlots()

    def __makePlot(self):
        self.plotWidget.plotData(self.ihs._variables, self.ihs._objective_function,
                                 self.ihs._varLowerBounds, self.ihs._varUpperBounds,
                                 self.__minMaxBandwidthValues, self.__trace)

    def __readParameters(self):
        fun = self.functionBox.text()
        iterations = self.iterationsBox.value()
        hms = self.hmsBox.value()
        hcmrMin = self.hcmrMinBox.value()
        hcmrMax = self.hcmrMaxBox.value()
        parMin = self.parMinBox.value()
        parMax = self.parMaxBox.value()
        bwMin = self.bwMinBox.value()
        bwMax = self.bwMaxBox.value()
        return fun, iterations, hms, \
            hcmrMin, hcmrMax, parMin, \
            parMax, bwMin, bwMax

    def __openFunctionChooseDialog(self):
        functionChooseDialog = FunctionChooseDialog()
        functionChooseDialog.setupUi()
        if functionChooseDialog.exec() == QDialog.Accepted:
            function = functionChooseDialog.getChosenFunction()
            self.functionBox.setText(function)

    def __nextButtonClicked(self):
        self.ihs = I_IHSAlgorithm(self.__readParameters())

        bandwidthDialog = BandwidthDialog()
        bandwidthDialog.setupUi(self.ihs.getVariables())
        if bandwidthDialog.exec() == QDialog.Accepted:
            self.__minMaxBandwidthValues = bandwidthDialog.getMinMaxValues()
            for i in range(len(self.ihs.getVariables())):
                self.ihs.setBounds(i, self.__minMaxBandwidthValues[i][0], self.__minMaxBandwidthValues[i][1])
            self.ihs.doYourTask()
            self.__printSolution()
            self.__trace = self.ihs.getTrace()
            self.__makePlot()

    def __disableButtonAndShowMessage(self):
        self.nextButton.setDisabled(True)
        self.statusbar.showMessage("Minimum musi być większe od maksimum!")

    def __enableButtonAndClearMessage(self):
        self.nextButton.setDisabled(False)
        self.statusbar.clearMessage()

    def __hcmrMaxValueChanged(self):
        if self.hcmrMaxBox.value() <= self.hcmrMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __hcmrMinValueChanged(self):
        if self.hcmrMaxBox.value() <= self.hcmrMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __parMinValueChanged(self):
        if self.parMaxBox.value() <= self.parMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __parMaxValueChanged(self):
        if self.parMaxBox.value() <= self.parMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __bwMinValueChanged(self):
        if self.bwMaxBox.value() <= self.bwMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __bwMaxValueChanged(self):
        if self.bwMaxBox.value() <= self.bwMinBox.value() + self.boxesValueOffset:
            self.__disableButtonAndShowMessage()
        else:
            self.__enableButtonAndClearMessage()

    def __functionValueChanged(self):
        string, err = evaluateError(self.functionBox.text())
        if err == 2:
            self.label_function_error.setStyleSheet("QLabel { color : red; }")
            self.nextButton.setDisabled(True)
            string = string[0]
        elif err == 0:
            self.label_function_error.setStyleSheet("QLabel { color : white; }")
            self.nextButton.setEnabled(True)
        else:
            self.label_function_error.setStyleSheet("QLabel { color : orange; }")
            self.nextButton.setDisabled(True)

        self.label_function_error.setText(QtCore.QCoreApplication.translate("MainWin", string))

    def __connectSlots(self):
        self.nextButton.clicked.connect(self.__nextButtonClicked)
        self.hcmrMaxBox.valueChanged.connect(self.__hcmrMaxValueChanged)
        self.hcmrMinBox.valueChanged.connect(self.__hcmrMinValueChanged)
        self.parMaxBox.valueChanged.connect(self.__parMaxValueChanged)
        self.parMinBox.valueChanged.connect(self.__parMinValueChanged)
        self.bwMaxBox.valueChanged.connect(self.__bwMaxValueChanged)
        self.bwMinBox.valueChanged.connect(self.__bwMinValueChanged)
        self.functionBox.textChanged.connect(self.__functionValueChanged)
        self.predefinedFunctionButton.clicked.connect(self.__openFunctionChooseDialog)

    def __printSolution(self):
        self.solutionBox.clear()
        functionValue, variables = self.ihs.getOptimalSolution()
        self.solutionBox.append(f'Wartość:\t{functionValue}')
        for var in variables:
            self.solutionBox.append(var)
