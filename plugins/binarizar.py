from PyQt5 import QtGui
import math

def executar(imagensP,statusbar):
    statusbar.showMessage("Rodando Binarização")
    for imagemP in imagensP.values(): binarizacao(imagemP)
    statusbar.showMessage("Binarização Finalizada")

threshold_values = {}#dicionario, como chave a cor do pixel de media e como valor a quantidade pixel afetados
h = [] #lista de histograma

def binarizacao(imagemP):
    h = gerar_hiatograma(imagemP.imagem)
    computar(h) #gerar uma lista de medias otimas para imagem
	
    op_thres = get_optimal_threshold() #pegar a media otima

    for x in range(imagemP.imagem.width()):
        for y in range(imagemP.imagem.height()):
            p1 = int(float(0.2989 * imagemP.imagem.pixelColor(x,y).red()) + float(0.5870 * imagemP.imagem.pixelColor(x,y).green()) + float(0.1140 * imagemP.imagem.pixelColor(x,y).blue()))
            if p1 <= 10:		
                cor = QtGui.QColor(0,0,0) 
                imagemP.imagem.setPixelColor(x,y,cor) #define a cor
            else:
                cor = QtGui.QColor(255,255,255) 
                imagemP.imagem.setPixelColor(x,y,cor) #define a cor
    imagemP.imagem.save(imagemP.caminho)
	
def gerar_hiatograma(imagem):
    for x in range(256):
        h.append(0.0)#preenchendo o histograma com zero , adicionando
		
    for x in range(imagem.width()):
        for y in range(imagem.height()):
            p1 = int(float(0.2989 * imagem.pixelColor(x,y).red()) + float(0.5870 * imagem.pixelColor(x,y).green()) + float(0.1140 * imagem.pixelColor(x,y).blue()))  # pegando o valor de cinza do pixel
            h[p1] += 1 #preencher o histograma com tons de cinza
    h[0] = 0.0 #serve pra ignorar o pixeis pretos, no calcular na media	pra n da um valor muito alto
    return h

def computar(h):
	cnt = countPixel(h) #contar o a quantidade de pixeis q tem na imagem 
	for i in range(1,len(h)): #retorna o tamanho	
		vb = variance(0, i) #variancia
		wb = wieght(0, i) / float(cnt) #peso
		vf = variance(i, len(h)) 
		wf = wieght(i, len(h)) / float(cnt)
		V2w = wb * (vb) + wf * (vf) #o quanto esse tom de cinza afeta minha img se eu usar ele  
		if not math.isnan(V2w):
			threshold_values[i] = V2w #colocando esse valor no dicionario de pesos otimos
        

def countPixel(h):
    cnt = 0
    for i in range(0, len(h)):
        if h[i]>0:
           cnt += h[i]
    return cnt 


def wieght(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    if w == 0: return 1.0
    return w #contar a quantidade de pixeis em um intervalo


def mean(s, e):
    m = 0
    w = wieght(s, e)
    for i in range(s, e):
        m += h[i] * i
    return m/float(w) #calcular media de pixei em um intervalo


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = wieght(s, e)
    for i in range(s, e):
        v += ((i - m) **2) * h[i]
    v /= w
    return v #retornar a viancia pra aquele intervalo de pixel

def get_optimal_threshold():
    min_V2w = min(threshold_values.values()) #retornar apenas o menor valor da lista
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]# percorre o dicionario procurando a chave(tom de cinza) que represente aquele valor
    return optimal_threshold[0] #retorna esse valor