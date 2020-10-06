from PyQt5 import QtCore, QtWidgets, QtGui

class FreeLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, image = None):
        super(FreeLabel, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.image = image
        self.w_o = self.image.width()
        self.h_o = self.image.height()
        self.clicked = False
        self.w = min(image.width(),800)
        self.h = min(image.height(),600)
        self.resize(self.w,self.h)
        self.cropPos = []

    def mouseMoveEvent(self, event):
        if self.clicked:
            pixels = self.getPixel(event.pos().x(),event.pos().y())
            self.cropPos.append([pixels[0],pixels[1]])
            self.image.setPixel(pixels[0],pixels[1], QtGui.QColor(0, 255, 255).rgb()) #cor da linha do recorte
            self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(self.w,self.h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        self.clicked = True

    def mouseDoubleClickEvent(self, event):
        self.clicked = False

    def getPixel(self,x,y):
        return [int((x*self.w_o)/self.w), int((y*self.h_o)/self.h)]

class RectLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, image = None,master = None, title = None):
        super(RectLabel, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.image = image
        self.master = master
        self.title = title
        self.w_o = self.image.width()
        self.h_o = self.image.height()
        self.w = min(image.width(),800)
        self.h = min(image.height(),600)
        self.resize(self.w,self.h)
        self.clicou = False
        self.cropPos = []

    def mousePressEvent(self, event):
        if len(self.cropPos) >= 2:
            return
        self.clicou = True
        self.cropPos.append([event.pos().x(),event.pos().y()])
        
        self.painter = QtGui.QPainter(self.image)
        self.painter.setBrush(QtGui.QColor(255,0,0)) #cor dos circulos
      
        point = self.getPixel(event.pos().x(),event.pos().y())

        self.painter.drawEllipse(point[0],point[1], 10, 10)# tamanho dos circulos
        self.painter.end()
        
        self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(self.w,self.h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
    
    def mouseMoveEvent(self, event):
        if self.clicou:
            point = [event.pos().x(),event.pos().y()]
            width = abs(self.cropPos[0][0]-point[0])
            height = abs(self.cropPos[0][1]-point[1]) #(20,23) - (78,56)
            
            self.master.setWindowTitle("{}x{} pixels ".format(width,height)+self.title)
              
    def getPixel(self,x,y):
        return [int((x*self.w_o)/self.w), int((y*self.h_o)/self.h)]
