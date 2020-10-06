from PyQt5 import QtGui

def executar(imagensP,statusbar):
    statusbar.showMessage("Aplicando Operadores")
    for imagemP in imagensP.values(): operadores(imagemP)
    statusbar.showMessage("Operadores Aplicados")
        
def operadores(imagemP):

    mascara = [
			[1, 1, 1],
			[1,1, 1],
			[1,1, 1]
	]

    imagem_old = [[0]*imagemP.imagem.height() for i in range(imagemP.imagem.width())]
	
    for x in range(imagemP.imagem.width()):
        for y in range(imagemP.imagem.height()):
            p1 = int(float(0.2989 * imagemP.imagem.pixelColor(x,y).red()) + float(0.5870 * imagemP.imagem.pixelColor(x,y).green()) + float(0.1140 * imagemP.imagem.pixelColor(x,y).blue()))  # pegando o valor de cinza do pixel
            imagem_old[x][y] = p1 #pegando o pixeis da img e colocando dentro da matriz
	
    imagem_nova = abertura(imagemP.imagem,imagem_old,mascara)#eliminar os detritos maiores da imagem
    imagem_nova = fechamento(imagemP.imagem,imagem_nova,mascara)#eliminar os detritos maiores da imagem
    for x in range(5):#o 5 é quantas vezes vou fazer a operação
        imagem_nova = dilatacao(imagem_nova,mascara,imagemP.imagem.width(),imagemP.imagem.height())#dilatação vai afinar certos pontos da img
    for x in range(5):
        imagem_nova = erosao(imagem_nova,mascara,imagemP.imagem.width(),imagemP.imagem.height())#a arosao vai alargar certos pontos da imagem
    

    for x in range(imagemP.imagem.width()):
        for y in range(imagemP.imagem.height()):
			# imp.set(x,y,imagem_nova[x][y])#salvando os processos na nova img
            cor = QtGui.QColor(int(imagem_nova[x][y]),int(imagem_nova[x][y]),int(imagem_nova[x][y])) 
            imagemP.imagem.setPixelColor(x,y,cor) #define a cor

    imagemP.imagem.save(imagemP.caminho) #atualiza img na interface


def erosao(imagem,mascara,width,height):
    new_img = [[0]*height for i in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):	
            new_img[i][j] = mascara[0][0]*imagem[i-1][j-1] and mascara[0][1]*imagem[i-1][j] and mascara[0][2]*imagem[i-1][j+1] \
             and mascara[1][0] * imagem[i][j - 1] and mascara[1][1]*imagem[i][j] and \
              mascara[1][2]*imagem[i][j+1] and mascara[2][0] * imagem[i+1][j - 1] and \
               mascara[2][1]*imagem[i+1][j] and mascara[2][2]*imagem[i+1][j+1]
    return new_img #aplicando a mascara nos pixeis vizinhos e no central..... quando for end vai pegar a ultima operação

def dilatacao(imagem,mascara,width,height):
	new_img = [[0]*height for i in range(width)]
	for i in range(1,width-1):
		for j in range(1,height-1):
			new_img[i][j] = mascara[0][0] * imagem[i - 1][j - 1] or mascara[0][1] * imagem[i - 1][j] or mascara[0][2] * \
             imagem[i - 1][j + 1] or mascara[1][0] * imagem[i][j - 1] or mascara[1][1] * imagem[i][j] or \
              mascara[1][2] * imagem[i][j + 1] or mascara[2][0] * imagem[i + 1][j - 1] or mascara[2][1] * \
               imagem[i + 1][j] or mascara[2][2] * imagem[i + 1][j + 1]
	return new_img #quando for or pega a primeira operação. dilatação vai afinar o objeto


def abertura(imp,imagem, mascara):
    image_1 = erosao(imagem, mascara,imp.width(),imp.height())
    image_2 = dilatacao(image_1, mascara,imp.width(),imp.height())
    return image_2


def fechamento(imp,imagem, mascara):
    image_1 = dilatacao(imagem, mascara,imp.width(),imp.height())
    image_2 = erosao(image_1, mascara,imp.width(),imp.height())
    return image_2

