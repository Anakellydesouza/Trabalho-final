from PyQt5 import QtGui

def executar(imagensP,statusbar):
    statusbar.showMessage("Rodando Mediana")
    for imagemP in imagensP.values(): mediana(imagemP)
    statusbar.showMessage("Mediana Aplicada")
        
def mediana(imagemP):
    mascara = [
        [1, -1, 1],
        [-1, 2, -1],
        [1, -1, 1]
    ]

    novo_pixel = []

    for x in range(imagemP.imagem.width()):  # prenchendo as linhas da mariz com zeros
        linha = []
        for y in range(imagemP.imagem.height()):
            linha.append(0)
        novo_pixel.append(linha)

    for x in range(imagemP.imagem.width()):  # pegando a media ponderada dos vizinhos de cada pixel e atribuindo aquele novo valor no pixel central
        for y in range(imagemP.imagem.height()):
            soma = (getpixel(imagemP.imagem,x-1, y-1) * mascara[0][0]) + (getpixel(imagemP.imagem,x, y-1) * mascara[0][1]) + (getpixel(imagemP.imagem,x+1, y-1) * mascara[0][2]) + (getpixel(imagemP.imagem,x-1, y) * mascara[1][0]) + (getpixel(imagemP.imagem,x, y-1) * mascara[1][1]) + (getpixel(imagemP.imagem,x+1, y) * mascara[1][2]) + (getpixel(imagemP.imagem,x-1, y+1) * mascara[2][0]) + (getpixel(imagemP.imagem,x, y+1) * mascara[2][1]) + (getpixel(imagemP.imagem,x+1, y+1) * mascara[2][2])
            soma = abs(int(soma))  # pegar valor absoluto caso seja negativo
            novo_pixel[x][y] = soma
            if novo_pixel[x][y] > 255:
                novo_pixel[x][y] = 255
            elif novo_pixel[x][y] < 0:
                novo_pixel[x][y] = 0

    for x in range(imagemP.imagem.width()):  # prenchendo a matris com os novos valores da media
        for y in range(imagemP.imagem.height()):
            cor = QtGui.QColor(int(novo_pixel[x][y]),int(novo_pixel[x][y]),int(novo_pixel[x][y])) 
            imagemP.imagem.setPixelColor(x,y,cor) #define a cor

    imagemP.imagem.save(imagemP.caminho)

def getpixel(imagem,x,y):
    p1 = int(float(0.2989 * imagem.pixelColor(x,y).red()) + float(0.5870 * imagem.pixelColor(x,y).green()) + float(0.1140 * imagem.pixelColor(x,y).blue()))  # pegando o valor de cinza do pixel
    return p1