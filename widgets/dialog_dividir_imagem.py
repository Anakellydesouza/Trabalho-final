from PyQt5 import QtCore, QtWidgets, QtGui
from widgets.label import RectLabel
import cv2

class DialogCanvasDividirImagem(QtWidgets.QDialog):
    def __init__(self, parent = None, imagemPath = None):
        super(DialogCanvasDividirImagem, self).__init__()

        imagem = QtGui.QImage(imagemPath)
        self.w = min(imagem.width(),800)
        self.h = min(imagem.height(),600)

        layout = QtWidgets.QVBoxLayout()

        buttonCrop = QtWidgets.QPushButton(self)
        buttonCrop.setText("Recortar")
        buttonCrop.clicked.connect(lambda: self.recortar(path = imagemPath))

        centralWidget = QtWidgets.QWidget(self)
        self.label = RectLabel(parent = centralWidget,image = imagem, master = self, title = "Recortando: " + imagemPath)
        self.label.setPixmap(QtGui.QPixmap.fromImage(imagem).scaled(self.w,self.h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        centralWidget.resize(self.w,self.h)

        layout.addWidget(buttonCrop)
        layout.addWidget(centralWidget)

        self.setLayout(layout)
        self.resize(self.w,self.h)
        self.setWindowTitle("Recortando: " + imagemPath)
        self.exec_()

    def recortar(self,path):
        if len(self.label.cropPos) != 2:
            return
        try:
            img = cv2.imread(path)

            img = cv2.resize(img,(self.w,self.h), interpolation = cv2.INTER_AREA)

            res = img[self.label.cropPos[0][1]:self.label.cropPos[1][1], self.label.cropPos[0][0]:self.label.cropPos[1][0]]

            self.label.cropPos = []
            self.label.clicou = False

            cv2.imshow("Recorte", res)

            caminho_imagem,_ = QtWidgets.QFileDialog.getSaveFileName(self,"Selecione onde salvar", "", "Imagem TIF (*.tif);; Imagem JPG (*.jpg)")
            if caminho_imagem:
                cv2.imwrite(caminho_imagem,res)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as error:
            self.label.cropPos = []
            self.label.clicou = False
