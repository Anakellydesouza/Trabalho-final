from PyQt5 import QtCore, QtWidgets, QtGui
from widgets.dialog_erro import DialogErro
import os

class DialogCriarClasse(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(DialogCriarClasse, self).__init__()

        self.parent = parent

        layout = QtWidgets.QVBoxLayout()

        centralWidget = QtWidgets.QWidget()
        layoutH = QtWidgets.QFormLayout()

        self.text = QtWidgets.QLineEdit(self)

        layoutH.addRow("Nome da classe: ",self.text)

        centralWidget.setLayout(layoutH)

        button = QtWidgets.QPushButton('Pronto', self)
        button.clicked.connect(self.criar) 

        layout.addWidget(centralWidget)
        layout.addWidget(button)

        self.setLayout(layout)
        self.resize(300,100)
        self.setWindowTitle("Escolha um nome para a pasta")
        self.exec_()

    def criar(self):
        pasta_classe = self.parent.caminho_backup+"\\"+self.text.text()
        print(pasta_classe)
        try:
            os.mkdir(pasta_classe)
        except OSError as error:
            DialogErro(message = error)
        else:
            self.close()
            self.parent.carregaImagens(caminho = self.parent.caminho_backup)
            self.parent.ui.statusbar.showMessage("Classe criada com sucesso",3)
       

    