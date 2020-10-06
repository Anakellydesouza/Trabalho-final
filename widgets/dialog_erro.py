from PyQt5 import QtCore, QtWidgets, QtGui

class DialogErro(QtWidgets.QMessageBox):
    def __init__(self, message = "Mensagem"):
        super(DialogErro, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.setText(message)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.setWindowTitle("Atenção")
        self.exec_()