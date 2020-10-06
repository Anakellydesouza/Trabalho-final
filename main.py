# UI importações
from PyQt5 import QtCore, QtWidgets, QtGui
import window

# plugins, modelos e widgets
from modelos.imagem import ImagemP

from plugins.plugins import *
from widgets.widgets import *

import os,shutil,sys

class Window(QtWidgets.QMainWindow):
    PESO_MAX = 10
    DEFAULT_PROJECAO = "TSNE"
    IMAGENS_CARREGADAS = False
    CORES_GRAFICO_D = [[166,206,227],[31,120,180],[178,223,138],[51,160,44]]
    CORES_GRAFICO =  [[31,120,180],[51,160,44],[227,26,28],[106,61,154],[166,206,227],[178,223,138],[251,154,153],[253,191,111],[255,127,0],[202,178,214],[255,255,153],[177,89,40]]
    def __init__(self):
        super(Window, self).__init__()
        self.ui = window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.width = QtWidgets.QDesktopWidget().width()
        self.height = QtWidgets.QDesktopWidget().height()-80

        self.daltonico = None
        self.isDaltonico = False
        self.imagensP = {}
        self.descritores = None
        self.caminho_backup = None
        self.caminho_sistema = os.path.abspath(os.path.dirname(__file__))       
        self.projecaoComparaX = []
        self.projecaoComparaY = []

        self.ui.menuFerramentas.hovered.connect(self.handleMenuHovered)
        self.ui.actionAbrir_Dataset.triggered.connect(lambda: self.carregaImagens(caminho = None))
        self.ui.actionPre_Processamento_Automatico.triggered.connect(self.executarPreProcessamento)
        self.ui.actionDeteccao_de_Caracteristicas.triggered.connect(self.executarDeteccao)
        self.ui.actionImagens.triggered.connect(self.exibirImagens)
        self.ui.actionSair.triggered.connect(lambda: sys.exit(0))
        self.ui.actionPCA.triggered.connect(lambda: self.executarProjecao(tipo = "PCA", callback = "menu"))
        self.ui.actionTSNE.triggered.connect(lambda: self.executarProjecao(tipo = "TSNE", callback = "menu"))
        self.ui.actionSAMMON.triggered.connect(lambda: self.executarProjecao(tipo = "SAMMON", callback = "menu"))
        self.ui.actionMDS.triggered.connect(lambda: self.executarProjecao(tipo = "MDS", callback = "menu"))
        self.ui.actionRecorteLivre.triggered.connect(self.exibirListaImagens)
        self.ui.actionDividir_Imagem.triggered.connect(self.dividirImagem)
        self.ui.actionCriar_Classe.triggered.connect(self.criarClasse)
        self.ui.actionEqualizacao.triggered.connect(lambda: self.executarFiltros(filtro = "equalizacao"))
        self.ui.actionMediana.triggered.connect(lambda: self.executarFiltros(filtro = "medianaw"))
        self.ui.actionBinarizacao.triggered.connect(lambda: self.executarFiltros(filtro = "binarizacao"))
        self.ui.actionInversao.triggered.connect(lambda: self.executarFiltros(filtro = "inversao"))
        self.ui.actionOperadores.triggered.connect(lambda: self.executarFiltros(filtro = "operadores"))

        self.ui.dockWidget_6.setMinimumSize(self.width/2,self.height/2.2)
        self.ui.dockWidget_7.setMinimumSize(self.width/2,self.height/2.2)
        self.ui.dockWidget_8.setMinimumSize(self.width/2,self.height/2.2)
        self.ui.dockWidget_9.setMinimumSize(self.width/2,self.height/2.2)

        self.showMaximized()
        self.ui.tableWidget.setVisible(False)

    def exibirImagens(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return

        self.carregaImagens(caminho = self.caminho_backup)

        DialogListaImagens(parent = self, imagensPpath = list(self.imagensP.keys()), onSelect = self.exibirImagemItem,title = "Selecione uma imagem para exibi-la.")

    def exibirImagemItem(self,imagePpath):
        WindowImage(parent = self, imagePpath = imagePpath)

    def handleMenuHovered(self, action):
        QtWidgets.QToolTip.showText(
            QtGui.QCursor.pos(), action.toolTip(),
            self.ui.menuFerramentas, self.ui.menuFerramentas.actionGeometry(action))

    def executarPreProcessamento(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return

        self.carregaImagens(caminho = self.caminho_backup)

        mediana.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        binarizacao.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        operadores.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)

    def executarFiltros(self, filtro):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return

        self.carregaImagens(caminho = self.caminho_backup)

        if filtro == "equalizacao":
            equalizacao.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        elif filtro == "mediana":
            mediana.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        elif filtro == "inversao":
            inversao.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        elif filtro == "binarizacao":
            binarizacao.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)
        elif filtro == "operadores":
            operadores.executar(imagensP = self.imagensP, statusbar = self.ui.statusbar)

    def criarClasse(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return
        DialogCriarClasse(self)
      
    def desenhaFrameDescritores(self):
        frame = FrameDescritores(parent = self.ui.dockWidget_6, width = self.width/2, height = self.height/2.2, descritores = self.descritores, pesoMax = self.PESO_MAX, onChanged = self.pesoAlterado)
        self.ui.dockWidget_6.setWidget(frame)

    def pesoAlterado(self,descritor,valor):
        self.descritores[descritor]['peso'] = valor/self.PESO_MAX
        self.executarProjecao(tipo = self.DEFAULT_PROJECAO, callback = "sliders")

    def exibirListaImagens(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return

        self.carregaImagens(caminho = self.caminho_backup)

        DialogListaImagens(parent = self, imagensPpath = list(self.imagensP.keys()), onSelect = self.exibirDialogCanvasRecorteLivre,title = "Selecione uma imagem para corta-la.")

    def criaBackup(self,destino): #raiz/pasta/ -> raiz/pasta_backup/
        shutil.copytree(self.caminho_backup,destino)
        self.ui.statusbar.showMessage("Backup completo, encontre seus dados em: {}".format(destino),3)

    def executarProjecao(self,tipo,callback):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return
            
        self.DEFAULT_PROJECAO = tipo
        projecao.executar(parent = self, coordenadas = [None,None], callback = callback)

    def desenhaFrameImagem(self,path): #desenhar quadro da imagem
        frame = FrameImage(parent = self.ui.dockWidget_9, pathImage = path, width = self.width/2, height = self.height/2)
        self.ui.dockWidget_9.setWidget(frame)

    def dividirImagem(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return
        
        caminho_imagem,_ = QtWidgets.QFileDialog.getOpenFileName(self,"Selecione uma imagem", "", "Tipos de Imagens (*.jpg *.png *.tif *.JPG  *.jpeg *.JPEG *.PNG)")
        
        if caminho_imagem:
            DialogCanvasDividirImagem(parent = self, imagemPath = caminho_imagem)

    def exibirDialogCanvasRecorteLivre(self,imagePpath):
        DialogCanvasRecorte(parent = self, imagePpath = imagePpath)

    def preencheTabela(self):
        linha = 0
        for imagemP in self.imagensP.values():
            self.ui.tableWidget.setItem(linha,0, QtWidgets.QTableWidgetItem(imagemP.nome))
            self.ui.tableWidget.setItem(linha,2, QtWidgets.QTableWidgetItem(imagemP.classe))
            self.ui.tableWidget.setItem(linha,1, QtWidgets.QTableWidgetItem("   "))
            self.ui.tableWidget.setColumnHidden(1,True)

            coluna = 3
            for descritor in imagemP.caracteristicas:
                if self.descritores[descritor]['checado']:
                    self.ui.tableWidget.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(round(imagemP.caracteristicas[descritor], 2))))
                    self.ui.tableWidget.setColumnHidden(coluna,False)
                else:
                    self.ui.tableWidget.setColumnHidden(coluna,True)
                coluna += 1
            linha += 1
        self.ui.tableWidget.itemClicked.connect(self.exibirImagem)

    def executarDeteccao(self):
        if not self.IMAGENS_CARREGADAS:
            self.ui.statusbar.showMessage("Carregue um dataset: Arquivo -> Dataset ou Ctrl-O",3)
            return

        self.carregaImagens(caminho = self.caminho_backup)

        self.ui.tableWidget.setVisible(True)
        self.ui.tableWidget.setRowCount(len(self.imagensP))

        caracteristicas.executar(imagensP = self.imagensP)

        self.descritores = DialogDescritores(descritores = list(self.imagensP.values())[0].caracteristicas, pesoMax = (self.PESO_MAX/10)).descritores

        self.preencheTabela()
        self.desenhaFrameDescritores()

    def exibirImagem(self):
        index = int(self.ui.tableWidget.currentRow())
        imagemP = list(self.imagensP.values())[index]
        self.desenhaFrameImagem(path = imagemP.caminho)

        if imagemP.xdata != None:
            projecao.executar(parent = self, coordenadas = [imagemP.xdata,imagemP.ydata], callback = "table")
                        
    def carregaImagens(self,caminho = None):
        self.IMAGENS_CARREGADAS = False
        self.daltonico = None
        self.imagensP = {}
        self.descritores = None
        self.caminho_backup = None
        self.caminho_sistema = os.path.abspath(os.path.dirname(__file__))       
        self.projecaoComparaX = []
        self.projecaoComparaY = []

        if caminho:
            self.caminho_backup = caminho
        else:
            self.daltonico = DialogDaltonico()
            
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            caminho_dados = QtWidgets.QFileDialog.getExistingDirectory(self,"Selecione uma pasta", "", options=options)
            self.caminho_backup = caminho_dados

            pastas_test = [(self.caminho_backup+"\\"+pasta) for pasta in os.listdir(self.caminho_backup) if os.path.isdir(self.caminho_backup+"\\"+pasta)]

            if self.daltonico != None:
                if self.daltonico.result == QtWidgets.QMessageBox.Yes:
                    self.isDaltonico = True
                    if len(pastas_test) > 4:
                        DialogErro("Modo daltônico ativado: Selecione apenas 4 classes")
                        return
                else:
                    self.isDaltonico = False
                    if len(pastas_test) > 12:
                        DialogErro("Limite de classes selecionadas é maior que o limite padrão de 12 classes")
                        return

            if self.caminho_backup:
                destino_backup = self.caminho_sistema+"\\{}_temp_{}".format(os.path.basename(self.caminho_backup),os.getpid())
                DialogBackupDados(message = "Um backup de seus dados será \ncriado em "+ destino_backup)
                if not os.path.isdir(destino_backup):
                    self.criaBackup(destino = destino_backup)
                    self.caminho_backup = destino_backup
            
        if self.caminho_backup:
            pastas = [(self.caminho_backup+"\\"+pasta) for pasta in os.listdir(self.caminho_backup) if os.path.isdir(self.caminho_backup+"\\"+pasta)]
            
    
            classe_id = 1
            for pasta in pastas:
                classe = os.path.basename(pasta)
                for arquivo in os.listdir(pasta):
                    caminho = pasta+"\\"+arquivo
                    self.imagensP[caminho] = ImagemP(caminho = caminho, classe = classe, classe_id = classe_id)
                classe_id += 1
        
        self.IMAGENS_CARREGADAS = True
        self.ui.statusbar.showMessage("Dataset Carregado")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()
    sys.exit(app.exec())          