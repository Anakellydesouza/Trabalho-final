from PyQt5 import QtCore, QtWidgets, QtGui

class FrameDescritores(QtWidgets.QScrollArea):
    def __init__(self,parent = None, width = None, height = None, descritores = None, pesoMax = None, onChanged = None):
        super(FrameDescritores, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setWidgetResizable(True)
        self.pesoMax = pesoMax
        self.onChanged = onChanged

        self.centralWidget = QtWidgets.QWidget()
        self.layoutGrid = QtWidgets.QGridLayout(self.centralWidget)
        coluna = 0
        for descritor in descritores.values():
            if descritor['checado']:
                self.insereSlider(descritor = descritor['nome'], coluna = coluna)
                label = QtWidgets.QLabel(self.centralWidget)
                label.setText(descritor['nome'])
                self.layoutGrid.addWidget(label, 0, coluna)
            coluna += 1
        self.setWidget(self.centralWidget)

    def insereSlider(self,descritor,coluna):
        widgetSlider = QtWidgets.QWidget(self.centralWidget)
        layout = QtWidgets.QHBoxLayout()
        slider = QtWidgets.QSlider(QtCore.Qt.Vertical, widgetSlider)
        slider.setFocusPolicy(QtCore.Qt.NoFocus) 
        slider.setTickPosition(QtWidgets.QSlider.TicksLeft)

        slider.setMaximum(self.pesoMax)
        slider.setMinimum(0)
        slider.setValue(self.pesoMax)
        
        slider.setSingleStep(1)
        slider.setTickInterval(1)

        slider.sliderReleased.connect(lambda: self.onChanged(descritor = descritor, valor = slider.value()))
        
        label = QtWidgets.QLabel(widgetSlider)
        label.setText("10\n\n9\n\n8\n\n7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1\n\n0") #numeros dos pesos dos sliders

        layout.addWidget(label)
        layout.addWidget(slider)
        widgetSlider.setLayout(layout)
        self.layoutGrid.addWidget(widgetSlider, 1, coluna)


        