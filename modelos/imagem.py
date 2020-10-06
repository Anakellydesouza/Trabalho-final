from PyQt5 import QtWidgets, QtGui
import os

class ImagemP:
    def __init__(self,caminho = None,classe = None, classe_id = None):
        self.caminho  = caminho
        self.imagem = QtGui.QImage(caminho)
        self.nome = os.path.basename(caminho)
        self.classe = classe
        self.classe_id = classe_id
        self.xdata = None
        self.ydata = None
        self.x = None
        self.y = None
        self.caracteristicas = None
