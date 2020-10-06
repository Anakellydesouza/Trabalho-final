from PyQt5 import QtCore, QtWidgets, QtGui

class DialogBackupDados(QtWidgets.QMessageBox):
    def __init__(self, message = "Mensagem"):
        super(DialogBackupDados, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setText(message)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.setWindowTitle("Atenção")
        self.exec_()