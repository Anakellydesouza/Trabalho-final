from PyQt5 import QtCore, QtWidgets, QtGui

class DialogListaImagens(QtWidgets.QMainWindow):
    def __init__(self, parent = None, imagensPpath = None, onSelect = None,title = None):
        super(DialogListaImagens, self).__init__(parent)
        self.onSelect = onSelect

        centralWidget = QtWidgets.QWidget(self)
        self.listWidget = QtWidgets.QListWidget(centralWidget)

        for item in imagensPpath: self.listWidget.insertItem(0,item)
        self.listWidget.clicked.connect(self.exibirImagem)
        
        self.listWidget.resize(500,500)
        centralWidget.resize(500,500)
        self.resize(500,500)
        self.setWindowTitle(title)
        self.show()

    def exibirImagem(self,index):
        item = self.listWidget.currentItem()
        self.onSelect(imagePpath = item.text())
        