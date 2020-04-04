# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bandwidthDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_bandwidthDialog(QDialog):
# class Ui_bandwidthDialog(object):

    def setupUi(self, bandwidthDialog):
        bandwidthDialog.setObjectName("bandwidthDialog")
        bandwidthDialog.resize(400, 300)

        self.retranslateUi(bandwidthDialog)
        QtCore.QMetaObject.connectSlotsByName(bandwidthDialog)

    def retranslateUi(self, bandwidthDialog):
        _translate = QtCore.QCoreApplication.translate
        bandwidthDialog.setWindowTitle(_translate("bandwidthDialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bandwidthDialog = QtWidgets.QDialog()
    ui = Ui_bandwidthDialog()
    ui.setupUi(bandwidthDialog)
    bandwidthDialog.show()
    sys.exit(app.exec_())
