from PyQt5 import QtCore, QtWidgets, QtGui
from widgets.label import FreeLabel
import cv2,numpy

class WindowImage(QtWidgets.QDialog):
    def __init__(self, parent = None, imagePpath = None):
        super(WindowImage, self).__init__()

        self.imagem = QtGui.QImage(imagePpath)
        
        self.w = min(self.imagem.width(),800)
        self.h = min(self.imagem.height(),600)

        self.label = QtWidgets.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.imagem).scaled(self.w,self.h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        
        self.label.resize(self.w,self.h)
        self.resize(self.w,self.h)
        
        self.setWindowTitle(imagePpath)
        self.exec_()
        