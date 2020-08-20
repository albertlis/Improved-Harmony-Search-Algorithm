from PyQt5.QtWidgets import QDialog
from ui.functionChooseDialog import Ui_dialog
from resource_path import resource_path

class FunctionChooseDialog(Ui_dialog, QDialog):
    def __init__(self):
        super(FunctionChooseDialog, self).__init__()

    def setupUi(self):
        super().setupUi(self)
        self.__connectSlots()
        self.__addFunctionsIntoBox()

    def __readFunctionsFromFile(self):
        try:
            file = open(resource_path("functions.txt"), 'r')
        except OSError as e:
            print(e)
            return None
        functions = file.read().splitlines()
        file.close()
        return functions

    def __addFunctionsIntoBox(self):
        functions = self.__readFunctionsFromFile()
        if functions is not None:
            for function in functions:
                self.functionBox.addItem(function)

    def __okButtonClicked(self):
        self.__chosenFunction = self.functionBox.currentText()
        self.accept()

    def __cancelButtonClicked(self):
        self.close()

    def __connectSlots(self):
        self.okButton.clicked.connect(self.__okButtonClicked)
        self.cancelButton.clicked.connect(self.__cancelButtonClicked)

    def getChosenFunction(self):
        return self.__chosenFunction
