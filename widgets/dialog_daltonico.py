from PyQt5 import QtCore, QtWidgets, QtGui

class DialogDaltonico(QtWidgets.QMessageBox):
    def __init__(self):
        super(QtWidgets.QMessageBox,self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.setText("Usar modo daltônico?")
        self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setWindowTitle("Preferências")
        self.result = self.exec_()