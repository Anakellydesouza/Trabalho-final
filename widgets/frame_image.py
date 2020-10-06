from PyQt5 import QtCore, QtWidgets, QtGui

class FrameImage(QtWidgets.QWidget):
    def __init__(self,parent = None, pathImage = None,width = None, height = None):
        super(FrameImage, self).__init__(parent)

        label = QtWidgets.QLabel(self)
        imagem = QtGui.QImage(pathImage)

        w = min(imagem.width(),width)
        h = min(imagem.height(),height)

        imagem = imagem.scaled(QtCore.QSize(w,h),QtCore.Qt.KeepAspectRatioByExpanding)

        label.setPixmap(QtGui.QPixmap.fromImage(imagem))
        self.resize(w,h)
        