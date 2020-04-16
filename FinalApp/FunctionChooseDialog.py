from PyQt5.QtWidgets import QDialog

from ui.functionChooseDialog import Ui_dialog


class FunctionChooseDialog(Ui_dialog, QDialog):
    def __init__(self):
        super(FunctionChooseDialog, self).__init__()

    def setupUi(self):
        super().setupUi(self)
        self.__connectSlots()

    def __okButtonClicked(self):
        self.accept()

    def __cancelButtonClicked(self):
        self.close()

    def __connectSlots(self):
        self.okButton.clicked.connect(self.__okButtonClicked)
        self.cancelButton.clicked.connect(self.__cancelButtonClicked)