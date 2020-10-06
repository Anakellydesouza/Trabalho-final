from PyQt5 import QtGui

def executar(imagensP,statusbar):
    statusbar.showMessage("Rodando Inversão")
    for imagemP in imagensP.values(): inversao(imagemP)
    statusbar.showMessage("Inversão Finalizada")

def inversao(imagemP):
    imagemP.imagem.invertPixels()
    imagemP.imagem.save(imagemP.caminho)
     