from PyQt5 import QtCore , QtWidgets, QtGui

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap

import math

def dist_euclidiana(v1, v2):
    dim, soma = len(v1), 0
    for i in range(dim):
        soma += math.pow(v1[i] - v2[i], 2)
    return math.sqrt(soma)

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=2, height=1, dpi=80):        
        fig = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)   
        super(MyMplCanvas, self).__init__(fig)
        
class MyStaticMplCanvas(MyMplCanvas):
    def mystatic(self, parent = None, dados = None, classes = None, coordenadas = None, cores = None, master = None, callback = None):
        
        self.setParent(master)
        ax1 = self.figure.add_subplot(121)
        ax1.clear()

        comparaXatual = []
        comparaYatual = []
        colors = []
        classes_label = []
        for imagemP in parent.imagensP.values():
            if not imagemP.classe in classes_label:
                classes_label.append(imagemP.classe)

        for rgb in cores.items():
            colors.append(QtGui.QColor(rgb[1][0],rgb[1][1],rgb[1][2],0).name())

        parent.ui.tableWidget.setColumnHidden(1,False)
        for linha in range(len(parent.imagensP)):
            rgb = cores[classes[linha]]
            parent.ui.tableWidget.item(linha,1).setBackground(QtGui.QColor(rgb[0],rgb[1],rgb[2],255))
        parent.ui.tableWidget.resizeColumnsToContents()

        
        scatter_c = ax1.scatter(dados[:, 0], dados[:, 1], alpha = .6, c = classes, cmap = ListedColormap(colors), picker = True)
        ax1.legend(handles = scatter_c.legend_elements()[0], labels = classes_label, bbox_to_anchor = (1.05, 1), loc = 'upper left', borderaxespad = 0.)
        
        data = scatter_c.get_offsets()       
        linha = 0
        for imagemP in parent.imagensP.values(): # salva na imagem os valores (coordenadas) dos descritores ja (normalizados, processados na projeção) e salva em uma lista local os valores (coordenas) para ser compara com a projeção anterior para verificar se houve mudança
            imagemP.xdata = data[linha][0]
            comparaXatual.append(data[linha][0])
            imagemP.ydata = data[linha][1]
            comparaYatual.append(data[linha][1])
            linha += 1

        if coordenadas[0]:
            ax1.scatter(coordenadas[0],coordenadas[1],s = 90,c = "#000000", alpha=.7,marker="x")

        if callback == "sliders" and len(parent.projecaoComparaX) > 0:
            if comparaXatual == parent.projecaoComparaX and comparaYatual == parent.projecaoComparaY:
                parent.ui.statusbar.showMessage("Não houve mudanças com a alteração do peso desse descritor.")
            else:
                if dist_euclidiana(comparaXatual,parent.projecaoComparaX) > 0.1 or dist_euclidiana(comparaYatual,parent.projecaoComparaY) > 0.1:
                    parent.ui.statusbar.showMessage("Houve mudanças significativas com a alteração do peso desse descritor.")
                else:
                    parent.ui.statusbar.showMessage("Houve mudanças pouco significativas com a alteração do peso desse descritor.")
        
        parent.projecaoComparaY = comparaYatual
        parent.projecaoComparaX = comparaXatual