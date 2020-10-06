from PyQt5 import QtGui

def executar(imagensP,statusbar):
    statusbar.showMessage("Rodando Equalização")
    for imagemP in imagensP.values(): equalizacao(imagemP)
    statusbar.showMessage("Equalização Finalizada")

def equalizacao(imagemP):
    histograma = {}  # dicionario
    for cor in range(256):
        histograma[cor] = 0  # iniciando todos os valores do histogramas com 0

    for x in range(imagemP.imagem.width()):
        for y in range(imagemP.imagem.height()):
            rgb = [0, 0, 0]
            p1 = int(float(0.2989 * imagemP.imagem.pixelColor(x,y).red()) + float(0.5870 * imagemP.imagem.pixelColor(x,y).green()) + float(0.1140 * imagemP.imagem.pixelColor(x,y).blue()))  # pegando o valor de cinza do pixel
            histograma[p1] = histograma[p1] + 1

    for x in range(256):
        #porcentagem de pixeis pra cada tom de cinza no histograma
        histograma[x] = histograma[x] / float(imagemP.imagem.width()*imagemP.imagem.height())

    for x in range(1, 256):
        #pegandado o pixel antingo e somando a probabilidade dele ser mais escuro
        histograma[x] = histograma[x] + histograma[x - 1]

    for x in range(256):
        # transformar ou normalizar a porcentagem para tons de cinza
        histograma[x] = histograma[x] * 255

    for x in range(imagemP.imagem.width()):
        for y in range(imagemP.imagem.height()):
            rgb = [0, 0, 0]
            p1 = int(float(0.2989 * imagemP.imagem.pixelColor(x,y).red()) + float(0.5870 * imagemP.imagem.pixelColor(x,y).green()) + float(0.1140 * imagemP.imagem.pixelColor(x,y).blue()))
            cor = QtGui.QColor(int(histograma[p1]),int(histograma[p1]),int(histograma[p1])) 
            imagemP.imagem.setPixelColor(x,y,cor) #define a cor
    imagemP.imagem.save(imagemP.caminho)