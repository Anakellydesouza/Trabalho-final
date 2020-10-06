from PyQt5 import QtGui
import os, random, math
from PIL import Image

import imagej
ij = imagej.init(r"C:\\Users\\Meus Documentos\\Desktop\\Fiji.app")
from jnius import autoclass
IJ = autoclass('ij.IJ')
ResultsTable = autoclass('ij.measure.ResultsTable')
ParticleAnalyzer = autoclass('ij.plugin.filter.ParticleAnalyzer')
ImageConverter = autoclass('ij.process.ImageConverter')


def generateCaracteristicas(imagemP):
    imagemP.caracteristicas = {
            'area': float(random.randint(0,400)),
            'perimetro': float(random.randint(0,400)),
            'media': float(random.randint(0,100)),
            "mediana": float(random.randint(0,100)),
            "angulo": float(random.randint(0,360)),
            "centroide y": float(random.randint(0,200)),
            "centroide x": float(random.randint(0,200)),
            "centro de massa x": float(random.randint(0,200)),
            "centro de massa y": float(random.randint(0,200)),
            "roi largura": float(random.randint(0,400)),
            "roi altura": float(random.randint(0,400)),
            "maximo": float(random.randint(0,200)),
            "minimo": float(random.randint(0,200)),
            'Mode': float(random.randint(0,100)),
            'X': float(random.randint(0,400)),
            'Y': float(random.randint(0,400)),
            'Width': float(random.randint(0,400)),
            'Height': float(random.randint(0,400)),
            'Major': float(random.randint(0,400)),
            'Minor': float(random.randint(0,400)),
            'Circ.': float(random.randint(0,200)),
            'Feret': float(random.randint(0,100)),
            'IntDen': float(random.randint(0,100)),
            'Skew': float(random.randint(0,100)),
            '%Area': float(random.randint(0,100)),
            'RawIntDen': float(random.randint(0,100)),
            'FeretX': float(random.randint(0,400)),
            'FeretY': float(random.randint(0,400)),
            'FeretAngle': float(random.randint(0,360)),
            'MinFeret': float(random.randint(0,400)),
            'AR': float(random.randint(0,200)),
            'Round': float(random.randint(0,100)),
            'Solidity': float(random.randint(0,100)),
            'MinThr': float(random.randint(0,100)),
            'MaxThr': float(random.randint(0,100)),
    }

def executar(imagensP):
    for imagemP in imagensP.values(): extrairCaracteristicas(imagemP)

def extrairCaracteristicas(imagemP):
    
    test = IJ.open(imagemP.caminho) #convesão da imagem pra 8 bits
    IJ.run(test, "8-bit", "")
    IJ.run(test, "Make Binary", "")
    IJ.run(test,"Convert to Mask","only")
    IJ.save(test,imagemP.caminho)

    imp = IJ.openImage(imagemP.caminho)
    ip = imp.getProcessor()

    descritores = imp.getAllStatistics()
    descritores_pa = {}
    rt = ResultsTable()
    pa = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE,ParticleAnalyzer.ALL_STATS,rt,0.0,9999.0)
    pa.analyze(imp,ip)
    for head in rt.getDefaultHeadings():
        if rt.columnExists(head):
            descritores_pa[head] = rt.getValue(rt.getColumnIndex(head),0)
        else:
            descritores_pa[head] = 0

    imagemP.caracteristicas = {
            'area':descritores_pa['Area'] if not math.isnan(float(descritores_pa['Area']))  else 0.0,
            'perimetro':descritores_pa['Perim.'] if not math.isnan(float(descritores_pa['Perim.']))  else 0.0,
            #'media':descritores_pa['Mean'] if not math.isnan(float(descritores_pa['Mean']))  else 0.0,
            #"mediana":descritores_pa['Median'] if not math.isnan(float(descritores_pa['Median']))  else 0.0,
            "angulo":descritores_pa['Angle'] if not math.isnan(float(descritores_pa['Angle']))  else 0.0,
            "centroide y":descritores_pa['BY'] if not math.isnan(float(descritores_pa['BY']))  else 0.0,
            "centroide x":descritores_pa['BX'] if not math.isnan(float(descritores_pa['BX']))  else 0.0,
            #"centro de massa x":descritores_pa['XM'] if not math.isnan(float(descritores_pa['XM']))  else 0.0,
            #"centro de massa y":descritores_pa['YM'] if not math.isnan(float(descritores_pa['YM']))  else 0.0,
            "roi largura":descritores.roiWidth if not math.isnan(float(descritores.roiWidth))  else 0.0,
            "roi altura":descritores.roiHeight if not math.isnan(float(descritores.roiHeight))  else 0.0,
           # "maximo":descritores_pa['Max'] if not math.isnan(float(descritores_pa['Max']))  else 0.0,
            #"minimo":descritores_pa['Min'] if not math.isnan(float(descritores_pa['Min']))  else 0.0,
            #'Mode':descritores_pa['Mode'] if not math.isnan(float(descritores_pa['Mode']))  else 0.0,
            #'X':descritores_pa['X'] if not math.isnan(float(descritores_pa['X']))  else 0.0,
            #'Y':descritores_pa['Y'] if not math.isnan(float(descritores_pa['Y']))  else 0.0,
            #'Width':descritores_pa['Width'] if not math.isnan(float(descritores_pa['Width']))  else 0.0,
            #'Height':descritores_pa['Height'] if not math.isnan(float(descritores_pa['Height']))  else 0.0,
            #'Major':descritores_pa['Major'] if not math.isnan(float(descritores_pa['Major']))  else 0.0,
            #'Minor':descritores_pa['Minor'] if not math.isnan(float(descritores_pa['Minor']))  else 0.0,
            'Circ.':descritores_pa['Circ.'] if not math.isnan(float(descritores_pa['Circ.']))  else 0.0,
            'Feret':descritores_pa['Feret'] if not math.isnan(float(descritores_pa['Feret']))  else 0.0,
            #'IntDen':descritores_pa['IntDen'] if not math.isnan(float(descritores_pa['IntDen']))  else 0.0,
            'Skew':descritores_pa['Skew'] if not math.isnan(float(descritores_pa['Skew']))  else 0.0,
            '%Area':descritores_pa['%Area'] if not math.isnan(float(descritores_pa['%Area']))  else 0.0,
            #'RawIntDen':descritores_pa['RawIntDen'] if not math.isnan(float(descritores_pa['RawIntDen']))  else 0.0,
            'FeretX':descritores_pa['FeretX'] if not math.isnan(float(descritores_pa['FeretX']))  else 0.0,
            'FeretY':descritores_pa['FeretY'] if not math.isnan(float(descritores_pa['FeretY']))  else 0.0,
            'FeretAngle':descritores_pa['FeretAngle'] if not math.isnan(float(descritores_pa['FeretAngle']))  else 0.0,
            'MinFeret':descritores_pa['MinFeret'] if not math.isnan(float(descritores_pa['MinFeret']))  else 0.0,
            'AR':descritores_pa['AR'] if not math.isnan(float(descritores_pa['AR']))  else 0.0,
            'Round':descritores_pa['Round'] if not math.isnan(float(descritores_pa['Round']))  else 0.0,
            'Solidity':descritores_pa['Solidity'] if not math.isnan(float(descritores_pa['Solidity']))  else 0.0,
            #'MinThr':descritores_pa['MinThr'] if not math.isnan(float(descritores_pa['MinThr']))  else 0.0,
            #'MaxThr':descritores_pa['MaxThr'] if not math.isnan(float(descritores_pa['MaxThr']))  else 0.0,
    }