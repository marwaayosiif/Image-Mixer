from PyQt5 import QtWidgets,QtGui
from mainwindow import Ui_MainWindow
import sys
import numpy as np
import logging
import cv2
from modesEnum import Modes
from imageModel import ImageModel 
QPixmap = QtGui.QPixmap


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.getFiles)
        self.diffOption=[]
        self.flag= 0
        self.ui.actionExit.triggered.connect(exit)
        self.options=[self.ui.option1,self.ui.option2]
        self.combobox = [self.ui.outputoptions,self.ui.imagechosen1,self.ui.imagechosen2,self.ui.compchosen1,self.ui.compchosen2]
        self.edits=[self.ui.edit1,self.ui.edit2]
        self.options[0].activated.connect(lambda:self.option(0))
        self.options[1].activated.connect(lambda:self.option(1))
        self.combobox[3].activated.connect(self.comboboxOptions)
        self.Slider=[self.ui.ratio1,self.ui.ratio2]
        self.outputs=[self.ui.imgoutput1,self.ui.imgoutput2]
        self.value1 = 0
        self.value2 = 0
        self.finalPicture=[]
        self.mag=["Options","Phase","uniform phase "]
        self.phase=["Options","Magnitude","uniform magnitude"]
        self.real=["Options","Imaginary"]
        self.imag=["Options","Real"]
        self.Slider[0].sliderReleased.connect(self.values)
        self.Slider[1].sliderReleased.connect(self.values)
        self.picture=[0, 0] 
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"    
        logging.basicConfig(filename='logging.log',level= logging.DEBUG,
                            format= LOG_FORMAT, filemode= 'w')
        self.logger = logging.getLogger()

    def comboboxOptions(self):
        if str(self.ui.compchosen1.currentText())=="uniform magnitude" or str(self.ui.compchosen1.currentText())=="Magnitude":
            self.ui.compchosen2.clear()
            self.ui.compchosen2.addItems(self.mag)
        elif str(self.ui.compchosen1.currentText())=="uniform phase " or str(self.ui.compchosen1.currentText())=="Phase":
            self.ui.compchosen2.clear()
            self.ui.compchosen2.addItems(self.phase) 
        elif str(self.ui.compchosen1.currentText())=="Real":
            self.ui.compchosen2.clear()
            self.ui.compchosen2.addItems(self.real)
        elif str(self.ui.compchosen1.currentText())=="Imaginary":
            self.ui.compchosen2.clear()
            self.ui.compchosen2.addItems(self.imag)    

    def uniform (self):
        if str(self.ui.compchosen2.currentText())=="Phase":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.h-1].mixUniform(self.picture[self.j-1],self.value2,Modes.uniformMagitudeAndPhase)
            self.showOutput(self.f,finalPicture)
        elif str(self.ui.compchosen2.currentText())=="uniform phase ":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.h-1].mixUniform(self.picture[self.j-1],self.value2,Modes.uniformMagitudeAnduniformPhase)
            self.showOutput(self.f,finalPicture)
        elif str(self.ui.compchosen2.currentText())=="Magnitude":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.h-1].mixUniform(self.picture[self.j-1],self.value2,Modes.uniformPhaseAndMagnitude)
            self.showOutput(self.f,finalPicture)
        elif  str(self.ui.compchosen2.currentText())=="uniform magnitude":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.h-1].mixUniform(self.picture[self.j-1],self.value2,Modes.uniformPhaseAnduniformMagnitude)
            self.showOutput(self.f,finalPicture)
        else:
            pass   

    def uniform1 (self):
        if  str(self.ui.compchosen2.currentText())=="uniform magnitude":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.j-1].mixUniform(self.picture[self.h-1],self.value1,Modes.uniformMagitudeAndPhase)
            self.showOutput(self.f,finalPicture)
        elif str(self.ui.compchosen2.currentText())=="uniform phase ":
            self.logger.info("The User is Choosing The Component")
            finalPicture= self.picture[self.j-1].mixUniform(self.picture[self.h-1],self.value1,Modes.uniformPhaseAndMagnitude)
            self.showOutput(self.f,finalPicture) 

    def values (self):
        self.h = self.ui.imagechosen1.currentIndex()
        self.j = self.ui.imagechosen2.currentIndex()
        self.logger.info("The User is Choosing The Image")
        if str(self.ui.outputoptions.currentText())=="Output 2":
            self.f=1
            self.logger.info("The User is Choosing Where To Show The Output")
        elif str(self.ui.outputoptions.currentText())=="Output 1":
            self.f=0
            self.logger.info("The User is Choosing Where To Show The Output")
        self.value1 = self.Slider[0].value()
        self.logger.info("The User is Getting The Value Of The First Slider")
        self.value2 = self.Slider[1].value()
        self.logger.info("The User is Getting The Value Of The Second Slider")

        if str(self.ui.compchosen1.currentText())=="Magnitude":
            self.logger.info("The User is Choosing The Component")
            finalPicture =self.picture[self.h-1].mix(self.picture[self.j-1],self.value1,self.value2,Modes.magnitudeAndPhase)
            self.showOutput(self.f,finalPicture)
            self.uniform1()
        elif str(self.ui.compchosen1.currentText())=="Real":
            self.logger.info("The User is Choosing The Component")
            self.finalPicture =self.picture[self.h-1].mix(self.picture[self.j-1],self.value1,self.value2,Modes.realAndImaginary)
            self.showOutput(self.f,self.finalPicture) 
        elif str(self.ui.compchosen1.currentText())=="Phase":
            self.logger.info("The User is Choosing The Component")
            finalPicture=self.picture[self.j-1].mix(self.picture[self.h-1],self.value2,self.value1,Modes.magnitudeAndPhase)
            self.showOutput(self.f,finalPicture)
            self.uniform1()
        elif str(self.ui.compchosen1.currentText())=="Imaginary":
            self.logger.info("The User is Choosing The Component")
            self.finalPicture =self.picture[self.j-1].mix(self.picture[self.h-1],self.value2,self.value1,Modes.realAndImaginary)
            self.showOutput(self.f,self.finalPicture)    
        elif str(self.ui.compchosen1.currentText())=="uniform magnitude":
            self.logger.info("The User is Choosing The Component")
            self.uniform()
        elif str(self.ui.compchosen1.currentText())=="uniform phase " :
            self.logger.info("The User is Choosing The Component")
            self.uniform()

    def getFiles(self):
        path,extention = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "") 
        if path == "":
            pass
        else:
            self.flag +=1
            self.logger.info("The User is Browsing")
            self.imageRead(path) 
            
    def imageRead(self,path):
        if self.flag == 1 :
            self.logger.info("The User is Opening The First Image")
            self.picture[0] = ImageModel(path)
            self.width =self.picture[0].imgByte.shape[0]
            self.height =self.picture[0].imgByte.shape[1]
            img = QPixmap(path)
            self.ui.img1.setPixmap(img)
        elif self.flag == 2 :
            self.picture[1] = ImageModel(path)
            if (self.picture[1].imgByte.shape[0]==self.width and self.picture[1].imgByte.shape[1]== self.height):
                img = QPixmap(path)
                if self.ui.img1.pixmap()== None :
                    self.ui.img1.setPixmap(img)
                elif self.ui.img2.pixmap()== None:
                    self.ui.img2.setPixmap(img)
                self.logger.info("The User is Opening The Second Image")     
            else :
                self.logger.info("The User is Trying To Insert Image Not Having The Same Type")
                self.ui.statusBar.showMessage("Sorry The Image Not Equal In Size !!")  
                self.flag -= 1  
        else :
            self.logger.info("The User is Inserting More Than One Image")
            self.ui.statusBar.showMessage("You Can Not Insert Another Image!!") 
    
    def option (self,i):
        if i in range(0,2):
            if str(self.options[i].currentText())=="FT Magnitude":
                x=self.picture[i].magnitudeInverse
                self.logger.info("The User is Viewing The Magnitude Only")
                self.ShowFourier(x,i)
            elif str(self.options[i].currentText())=="FT Phase":
                x=self.picture[i].phaseInverse
                self.logger.info("The User is Viewing The Phase Only")
                self.ShowFourier(x,i)
            elif str(self.options[i].currentText())=="FT Real component":
                x=self.picture[i].real
                self.logger.info("The User is Viewing The Real Only")
                self.ShowFourier(x,i)
            elif str(self.options[i].currentText())=="FT Imaginary component":
                x=self.picture[i].imaginary
                self.logger.info("The User is Viewing The Imaginary Only")
                self.ShowFourier(x,i)
           
    def ShowFourier (self,k,i):
        cv2.imwrite('SavedImage.jpg',k)
        im2 = QPixmap('SavedImage.jpg')
        self.edits[i].setPixmap(im2) 
        
    def showOutput (self,i,picture):
        cv2.imwrite('SavedImage.jpg',picture)
        im2 = QPixmap('SavedImage.jpg')
        self.outputs[i].setPixmap(im2)    

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
     
