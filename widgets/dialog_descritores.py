from PyQt5 import QtCore, QtWidgets, QtGui

class DialogDescritores(QtWidgets.QDialog):
    def __init__(self,descritores = None, pesoMax = None):
        super(DialogDescritores, self).__init__()
        self.descritores = {}
        
        layoutV = QtWidgets.QVBoxLayout()
        scrollarea = QtWidgets.QScrollArea(self)
        scrollarea.setFixedHeight(300)
        scrollarea.setFixedWidth(250)
        scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        centralWidget = QtWidgets.QWidget()
        layoutV_2 = QtWidgets.QVBoxLayout(centralWidget)

        for descritor in descritores:
            check = QtWidgets.QCheckBox(descritor,centralWidget)
            layoutV_2.addWidget(check) 
            check.setChecked(True)
            self.descritores[descritor] = {"nome": descritor,"widget":check,"checado":True, "peso": pesoMax}

        scrollarea.setWidget(centralWidget)

        button = QtWidgets.QPushButton('Pronto', self)
        button.clicked.connect(self.finalizar)
        button_2 = QtWidgets.QPushButton('Desmarcar Todos', self)
        button_2.clicked.connect(lambda: self.alteraTodos(False))
        button_3 = QtWidgets.QPushButton('Marcar Todos', self)
        button_3.clicked.connect(lambda: self.alteraTodos(True))

        layoutV.addWidget(scrollarea)
        layoutV.addWidget(button_2)
        layoutV.addWidget(button_3)
        layoutV.addWidget(button)

        self.setLayout(layoutV)
        self.setWindowTitle("Selecione os descritores")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.exec_()

    def alteraTodos(self,estado):
        for descritor in self.descritores.values():
            descritor["widget"].setChecked(estado)
            descritor["checado"] = estado

    def finalizar(self):
        for descritor in self.descritores.values():
            if descritor["widget"].isChecked():
                descritor["checado"] = True
            else:
                descritor["checado"] = False
        self.close()
