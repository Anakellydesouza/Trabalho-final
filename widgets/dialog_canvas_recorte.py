from PyQt5 import QtCore, QtWidgets, QtGui
from widgets.label import FreeLabel
import cv2,numpy

class DialogCanvasRecorte(QtWidgets.QDialog):
    def __init__(self, parent = None, imagePpath = None):
        super(DialogCanvasRecorte, self).__init__()

        imagem = QtGui.QImage(imagePpath)

        layout = QtWidgets.QVBoxLayout()

        buttonCrop = QtWidgets.QPushButton(self)
        buttonCrop.setText("Recortar")
        buttonCrop.clicked.connect(lambda: self.recortar(path = imagePpath))

        buttonCrop2 = QtWidgets.QPushButton(self)
        buttonCrop2.setText("Recortar 2")
        buttonCrop2.clicked.connect(lambda: self.recortar2(path = imagePpath))

        centralWidget = QtWidgets.QWidget(self)
        self.label = FreeLabel(parent = centralWidget,image = imagem)
        self.label.setPixmap(QtGui.QPixmap.fromImage(imagem).scaled(self.label.w,self.label.h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        centralWidget.resize(self.label.w,self.label.h)

        layout.addWidget(buttonCrop)
        layout.addWidget(buttonCrop2)
        layout.addWidget(centralWidget)

        self.setLayout(layout)
        self.resize(self.label.w+60,self.label.h+50)
        self.setWindowTitle("Recortando: " + imagePpath)
        self.exec_()

    def recortar(self,path):
        if len(self.label.cropPos) <= 2:
            return
        self.img = cv2.imread(path)
        

        mask = numpy.zeros(shape = self.img.shape[0:2],dtype=numpy.uint8)
        points = numpy.array(self.label.cropPos)

        cv2.drawContours(mask, [points], -1, 127, -1, cv2.LINE_AA)
        mask[mask == 0] = 1
        mask[mask == 127] = 0

        res = cv2.bitwise_and(1,self.img,self.img,mask = mask)

        self.label.cropPos = []
        self.close()
        
        #height, width, channels = self.img.shape
        #if width > 600:
         #   res = cv2.resize(res, (600, int((height*600)/width)))
            
        cv2.imshow("Recorte", res)
        cv2.imwrite(path,res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def recortar2(self,path):
        if len(self.label.cropPos) <= 2:
            return
        self.img = cv2.imread(path)
        
        mask = numpy.zeros(shape = self.img.shape[0:2],dtype=numpy.uint8)
        mask2 = 255 * numpy.ones(shape = self.img.shape[0:2],dtype=numpy.uint8)
        points = numpy.array(self.label.cropPos)

        cv2.drawContours(mask, [points], -1, 127, -1, cv2.LINE_AA)
        mask[mask == 0] = 1
        mask[mask == 127] = 0

        res = cv2.bitwise_and(1,mask2,mask2,mask = mask)

        self.label.cropPos = []
        self.close()
        
       # height, width, channels = self.img.shape
        #if width > 600:
         #   res = cv2.resize(res, (600, int((height*600)/width)))

        cv2.imshow("Recorte", res)
        cv2.imwrite(path,res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        