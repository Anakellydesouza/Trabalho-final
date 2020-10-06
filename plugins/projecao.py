from PyQt5 import QtCore , QtWidgets, QtGui
from widgets.grafico_projecao import MyStaticMplCanvas

## imports dos algoritmos de projeção
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
import plugins.sammon as SAMMON

# demais importações
import numpy
from scipy import stats

def executar(parent = None, coordenadas = None, callback = None):
    parent.ui.statusbar.showMessage("Calculando pesos dos descritores...")

    dset_i = []
    x_i = []
    classes_i = []
    valores = []
    cores = {}

    for imagemP in parent.imagensP.values(): # pega os valores dos descritores e classes dos individuos e se marcado normaliza eles
        if parent.ui.actionNormalizar_Valores.isChecked():
            descritores_valores = numpy.array(list(imagemP.caracteristicas.values()))
            valores.append( stats.zscore( a = descritores_valores).tolist())
        else:
            descritores_valores = list(imagemP.caracteristicas.values())
            valores.append( descritores_valores)
        classes_i.append(imagemP.classe_id)

    linha = 0
    for imagemP in parent.imagensP.values():# multiplica os valores com os seus pesos
        coluna = 0
        for descritor in imagemP.caracteristicas:
            valores[linha][coluna] = imagemP.caracteristicas[descritor] * parent.descritores[descritor]['peso']
            coluna += 1
        x_i.append(valores[linha])
        linha += 1

    dset_i.append(x_i)
    dset_i.append(classes_i)
    X, classes = dset_i
    if parent.isDaltonico == True:
        cores_geral = parent.CORES_GRAFICO_D
    else:
        cores_geral = parent.CORES_GRAFICO
    for cor_index in range(len(sorted(set(classes_i)))): # define as cores das classes
        cores[cor_index+1] = cores_geral[cor_index]

    if parent.DEFAULT_PROJECAO == "PCA": # roda o algoritmo de projeção definido
        pca = PCA(n_components=2, whiten=False)
        Y = pca.fit(X).transform(X)
    elif parent.DEFAULT_PROJECAO == "TSNE":
        tsne = TSNE(n_components=2,random_state = 0)
        Y = tsne.fit_transform(X)
    elif parent.DEFAULT_PROJECAO == "MDS":
        mds = MDS(n_components=2,random_state = 0)
        Y = mds.fit_transform(X)
    elif parent.DEFAULT_PROJECAO == "SAMMON":
        Y = SAMMON.sammon(data = numpy.array(X),target_dim = 2)[0]
    else:
        pca = PCA(n_components=2, whiten=False)
        Y = pca.fit(X).transform(X)

    # exibe o grafico com os dados da projeçao
    grafico = MyStaticMplCanvas(width=int((parent.width/2)/80)+1, height= int((parent.height/2.2)/80)+1 ,dpi=80)
    grafico.mystatic(
        master = parent.ui.dockWidgetContents_8,
        dados = Y,
        classes = classes,
        coordenadas = coordenadas,
        cores = cores,
        parent = parent,
        callback = callback)

    grafico.mpl_connect('pick_event', lambda e: onClick(e,parent = parent))
    grafico.show()

def onClick(event,parent):
    index = event.ind
    coordenadas = event.artist.get_offsets()
    linha = 0
    for imagemP in parent.imagensP.values():
        if imagemP.xdata == coordenadas[index][0][0] and imagemP.ydata == coordenadas[index][0][1]:
            parent.desenhaFrameImagem(path = imagemP.caminho)
            parent.ui.tableWidget.selectRow(linha)
            executar(parent = parent, coordenadas = [imagemP.xdata,imagemP.ydata], callback = "table")
            break
        linha += 1