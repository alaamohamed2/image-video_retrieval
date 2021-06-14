#import
import os
import sys
import cv2 as cv
import numpy as np
import matplotlib as mt
import matplotlib.pyplot as plt
import PyQt5 as qt
import PyQt5.QtCore
import PyQt5.QtWidgets as qwd
import re
import math
import shutil
import datetime
import inspect
from color.color import ColorDescriptor
from gabor.gabor import GaborDescriptor
from hog.hog import HOGDescriptor
from vgg16.vgg16 import VGGNet


from searcher import Searcher
from time import sleep
from PyQt5.QtNetwork import *
from PyQt5 import QtGui as gui
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)

# fileName=""
videoPath=""
##MACRO DEFINITIONS 
WINDOW_TITLE="MultiMediaProject"
WINDOW_SIZE_X=1280#1920
WINDOW_SIZE_Y=720#1080
WINDOW_SMALL_TITLE="Select Recursive Feedback"
QDIALOG_IMAGE_PREFIX_TYPE = "*.png *.jpg *.jpeg *.JPG"
QDIALOG_IAMGE_SELECTION_DIALOG_NAME="Select image"
SecondUIButtonNames = []
SECOND_GUI_ICON_NAME_PATH="align.png"

class PicButton(qwd.QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = gui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()




class firstGui(qwd.QDialog):
    
    def __init__(self, parent=None):
        super(firstGui, self).__init__(parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(0, 0, 600, 600)
        self.InitUI()

    def InitUI(self):
       
        ####Label OpenImg 
        logData("creating main UI") 
        
        self.setStyleSheet(""" firstGui{background-image: url("logo.JPG");   background-repeat: no-repeat; 
       background-position: center;}""")
        
       
        btnClose = qwd.QPushButton('Close', self)
        btnClose.setToolTip("Close Program")
        btnClose.clicked.connect(self.BtnCloseSystem)
        btnClose.setStyleSheet("QPushButton"
                             "{"
                             "background-color : red ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )

        ##button open image
        btnOpenImage = qwd.QPushButton("Image", self)
        btnOpenImage.clicked.connect(self.ButtonImage)
        btnOpenImage.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue ;color : black; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button open video 
        btnOpenVideo = qwd.QPushButton("Video",self)
        btnOpenVideo.setToolTip("This button opens the images from google web services")
        btnOpenVideo.clicked.connect(self.ButtonVideo)
        btnOpenVideo.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue ;color : black; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )

        ####layouts
        lytQHBtns=qwd.QHBoxLayout() 
        lytQHBtns.addWidget(btnOpenImage)
        lytQHBtns.addWidget(btnOpenVideo)
        lytQHBtns.addWidget(btnClose)
        ##Box Layout
        #image
        lytQBoxImg=qwd.QBoxLayout(qwd.QBoxLayout.TopToBottom, parent=None)
        # lytQBoxImg.addWidget(self.lblOpenImg)
        lytQVImg=qwd.QVBoxLayout()
        lytQVImg.addLayout(lytQBoxImg)
        ##Line Edit + Lbl Layout
        lytQVLnedsAndLabels = qwd.QVBoxLayout()
        ####Grid Layout
        lytQGridMain = qwd.QGridLayout()
        # lytQGridMain.addLayout(lytQVImg, 1, 0, 6, 1)
        # lytQGridMain.addLayout(lytQVLnedsAndLabels, 1, 0)
        # lytQGridMain.addLayout(lytQBoxTxt, 8, 0, 6, 1)
        lytQGridMain.addLayout(lytQHBtns, 7, 0)
        self.setLayout(lytQGridMain)

    def ButtonVideo(self):
 

        GUI2=VideoGui(self)
        GUI2.show()


    def BtnCloseSystem(self):
        sys.exit()

    def ButtonImage(self):
           dialog = QGui(self)
           dialog.show()


    def GetAndSetImg(self,file_name):
        try:        
            self.matImg= cv.imread(file_name[0])
            self.image_path=file_name[0]
            self.image_paths_len=3

            self.SetSystemSearchedFlag(True)
            matRGBImg=cv.cvtColor(self.matImg, cv.COLOR_BGR2RGB)
            Qimg = gui.QImage(matRGBImg.data, matRGBImg.shape[1], matRGBImg.shape[0], gui.QImage.Format_RGB888)
            pixelImg = gui.QPixmap.fromImage(Qimg)
            self.lblOpenImg.setPixmap(pixelImg)
        except Exception as ex:
            logData("Exception on "+ str(ex))
            self.txtSystemStatus.append("Exception on "+ str(ex))
            
    def SetSystemSearchedFlag(self,flag):
        self.isSystemSearched=flag

   
class VideoGui(qwd.QDialog):
    def __init__(self, parent=None):
        super(VideoGui, self).__init__(parent)
        self.setWindowTitle("Video")
        self.setGeometry(0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.InitUI()
        self.setStyleSheet("* {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"
                       "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 white, stop:1 lightblue);}")

    def InitUI(self):
        ####Label OpenImg  
        self.lblOpenImg = qwd.QLabel('', self)
        self.lblOpenImg.setEnabled(True)
        self.lblOpenImg.setGeometry(20, 100, 500, 300)
        self.lblOpenImg.setSizePolicy(qwd.QSizePolicy.Ignored, qwd.QSizePolicy.Ignored)
        self.lblOpenImg.setScaledContents(True)
        self.lblOpenImg.setAutoFillBackground(True)
        self.lblOpenImg.setFrameShape(qwd.QFrame.Panel)
        self.lblOpenImg.setFrameShadow(qwd.QFrame.Plain)
        self.lblOpenImg.setLineWidth(2)
        ####Text Box Definitions
        ##text system status
        self.txtSystemStatus = qwd.QTextBrowser(self)
        self.txtSystemStatus.setGeometry(500, 200, 400, 300)
        self.txtSystemStatus.setOpenExternalLinks(True)
        self.txtSystemStatus.setAcceptRichText(True)
        self.txtSystemStatus.setMouseTracking(True)
        ##global txtSystemStatus
        ####Button Definitions
        ##Button Close
        btnClose = qwd.QPushButton('Close', self)
        btnClose.setToolTip("Close Program")
        btnClose.clicked.connect(self.BtnCloseSystem)
        btnClose.setStyleSheet("QPushButton"
                             "{"
                             "background-color : red ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button open image
        btnOpenImage = qwd.QPushButton("Open and retrive Video", self)
        btnOpenImage.setToolTip("Open image for signal processing")
        btnOpenImage.clicked.connect(self.ButtonOpenVideo)
        btnOpenImage.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
    
    
        ####layouts
        lytQHBtns=qwd.QHBoxLayout() 
        lytQHBtns.addWidget(btnOpenImage)

        lytQHBtns.addWidget(btnClose)
        ##Box Layout
        #system status
        lytQBoxTxt=qwd.QBoxLayout(qwd.QBoxLayout.LeftToRight, parent=None)
        lytQBoxTxt.addWidget(self.txtSystemStatus)
        lytQBoxTxt.setGeometry(QtCore.QRect(200, 200, 100, 300))
        #image
        lytQBoxImg=qwd.QBoxLayout(qwd.QBoxLayout.LeftToRight, parent=None)
        lytQBoxImg.addWidget(self.lblOpenImg)
        lytQVImg=qwd.QVBoxLayout()
        lytQVImg.addLayout(lytQBoxImg)
        ##Line Edit + Lbl Layout
        lytQVLnedsAndLabels = qwd.QVBoxLayout()
        ####Grid Layout
        lytQGridMain = qwd.QGridLayout()
        lytQGridMain.addLayout(lytQVImg, 1, 0, 6, 1)
        lytQGridMain.addLayout(lytQVLnedsAndLabels, 1, 0)
        lytQGridMain.addLayout(lytQBoxTxt, 8, 0, 0, 1)
        lytQGridMain.addLayout(lytQHBtns, 7, 0)
        self.setLayout(lytQGridMain)

    def VideoAlgorithm(self):
        GUI2=QGuiSmall(self)
        GUI2.show()
        
    


    def BtnCloseSystem(self):
        sys.exit()

    def ButtonOpenVideo(self):
        player = VideoPlayer(self)

        player.setWindowTitle("Player")
        # player.resize(400, 400)
        player.setGeometry(300, 70, 700, 500)
        player.show()   


    def GetAndSetImg(self,file_name):
        try:        
            self.matImg= cv.imread(file_name[0])
            self.image_path=file_name[0]
            self.image_paths_len=3
            #self.trainData(matImg)
    
            # organizeFile(GOOGLE_GIMAGE_OUTPUT_PATH+searchList[svmPrediction]+"/",".jpg",'temp_')
            # setForRetrivalFileNames( GOOGLE_GIMAGE_OUTPUT_PATH+searchList[svmPrediction],svmPrediction)
            self.SetSystemSearchedFlag(True)
            matRGBImg=cv.cvtColor(self.matImg, cv.COLOR_BGR2RGB)
            Qimg = gui.QImage(matRGBImg.data, matRGBImg.shape[1], matRGBImg.shape[0], gui.QImage.Format_RGB888)
            pixelImg = gui.QPixmap.fromImage(Qimg)
            self.lblOpenImg.setPixmap(pixelImg)
        except Exception as ex:
            logData("Exception on "+ str(ex))
            self.txtSystemStatus.append("Exception on "+ str(ex))
            
    def SetSystemSearchedFlag(self,flag):
        self.isSystemSearched=flag









class QGui(qwd.QDialog):
    
    def __init__(self, parent=None):
        self.fileName=''
        super(QGui, self).__init__(parent)
        self.setWindowTitle("Image")
        self.setGeometry(0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.InitUI()
        self.setStyleSheet("* {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"
                       "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 white, stop:1 lightblue);}")

    def InitUI(self):
        ####Label OpenImg 
        logData("creating main UI") 
        self.lblOpenImg = qwd.QLabel('', self)
        self.lblOpenImg.setEnabled(True)
        self.lblOpenImg.setGeometry(20, 100, 500, 300)
        self.lblOpenImg.setSizePolicy(qwd.QSizePolicy.Ignored, qwd.QSizePolicy.Ignored)
        self.lblOpenImg.setScaledContents(True)
        self.lblOpenImg.setAutoFillBackground(True)
        self.lblOpenImg.setFrameShape(qwd.QFrame.Panel)
        self.lblOpenImg.setFrameShadow(qwd.QFrame.Plain)
        self.lblOpenImg.setLineWidth(2)
        ####Text Box Definitions
        ##text system status
        self.txtSystemStatus = qwd.QTextBrowser(self)
        self.txtSystemStatus.setGeometry(500, 200, 400, 300)
        self.txtSystemStatus.setOpenExternalLinks(True)
        self.txtSystemStatus.setAcceptRichText(True)
        self.txtSystemStatus.setMouseTracking(True)
        ##global txtSystemStatus
        ####Button Definitions
        ##Button Close
        btnClose = qwd.QPushButton('Close', self)
        btnClose.setToolTip("Close Program")
        btnClose.clicked.connect(self.BtnCloseSystem)
        btnClose.setStyleSheet("QPushButton"
                             "{"
                             "background-color : red ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button for opening image
        btnOpenImage = qwd.QPushButton("Open Image", self)
        btnOpenImage.setToolTip("")
        btnOpenImage.clicked.connect(self.BtnOpenImage)
        btnOpenImage.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button for shape
        retriveByShapeBtn = qwd.QPushButton("By Shape",self)
        retriveByShapeBtn.setToolTip("")
        retriveByShapeBtn.clicked.connect(self.retriveImageByShape)
        retriveByShapeBtn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button for histogram
        retriveByHistogram2Btn = qwd.QPushButton("By histogram",self)
        retriveByHistogram2Btn.setToolTip("")
        retriveByHistogram2Btn.clicked.connect(self.retriveImageByHisto2)
        retriveByHistogram2Btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )                     
        ##button for color 
        retriveByColorBtn= qwd.QPushButton("By Color",self)
        retriveByColorBtn.setToolTip("")
        retriveByColorBtn.clicked.connect(self.retriveImageByColor)
        retriveByColorBtn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )
        ##button for texture 
        retriveByTextureBtn= qwd.QPushButton("By textutre",self)
        retriveByTextureBtn.setToolTip("")
        retriveByTextureBtn.clicked.connect(self.retriveImageByTexture)  
        retriveByTextureBtn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : grey ;color : white; border-radius: 10 ; border-color : black; border-width: 2px; border-bottom: 2px solid ;padding : 8;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             
                            
                             "}"
                             )      
        ####layouts
        lytQHBtns=qwd.QHBoxLayout() 
        lytQHBtns.addWidget(btnOpenImage)
        lytQHBtns.addWidget(retriveByShapeBtn)
        lytQHBtns.addWidget(retriveByHistogram2Btn)
        lytQHBtns.addWidget(retriveByColorBtn)
        lytQHBtns.addWidget(retriveByTextureBtn)
        lytQHBtns.addWidget(btnClose)
        ##Box Layout
        #system status
        lytQBoxTxt=qwd.QBoxLayout(qwd.QBoxLayout.LeftToRight, parent=None)
        lytQBoxTxt.addWidget(self.txtSystemStatus)
        lytQBoxTxt.setGeometry(QtCore.QRect(200, 200, 100, 300))
        #image
        lytQBoxImg=qwd.QBoxLayout(qwd.QBoxLayout.LeftToRight, parent=None)
        lytQBoxImg.addWidget(self.lblOpenImg)
        lytQVImg=qwd.QVBoxLayout()
        lytQVImg.addLayout(lytQBoxImg)
        ##Line Edit + Lbl Layout
        lytQVLnedsAndLabels = qwd.QVBoxLayout()
        ####Grid Layout
        lytQGridMain = qwd.QGridLayout()
        lytQGridMain.addLayout(lytQVImg, 1, 0, 6, 1)
        lytQGridMain.addLayout(lytQVLnedsAndLabels, 1, 0)
        lytQGridMain.addLayout(lytQBoxTxt, 8, 0, 0, 1)
        lytQGridMain.addLayout(lytQHBtns, 7, 0)
        self.setLayout(lytQGridMain)


     
        
    
    def retriveImageByColor(self):
       

        os.system("python search.py --query "+str(self.fileName[0])[2:-2]  +" --c color")


    def retriveImageByTexture(self):
       

        os.system("python search.py --query "+str(self.fileName[0])[2:-2]  +" --c gabor")


    def retriveImageByShape(self):
       
        os.system("python search.py --query "+str(self.fileName[0])[2:-2]  +" --c hog")
    
    def retriveImageByHisto2(self):
       print("")
       os.system("python search_histo.py --index index.csv --query "+str(self.fileName[0])[2:-2]  +" --result-path ./database")    


    def BtnCloseSystem(self):
        sys.exit()

    def BtnOpenImage(self):
        self.fileName=qwd.QFileDialog.getOpenFileNames(self,QDIALOG_IAMGE_SELECTION_DIALOG_NAME,"",QDIALOG_IMAGE_PREFIX_TYPE) 
        
        print(self.fileName)       
        self.folderName=os.path.dirname(str(self.fileName[0]).split("'",1)[1])
        if not self.fileName:
            self.txtSystemStatus.setText("Please Select a jpg or png file")
        else:  
            self.txtSystemStatus.setText("The file path " + str(self.fileName[0]) + " is selected ")
            logData("the file path "+ str(self.fileName[0])[2:-2] + " is selected ")
            self.txtOpenFilePath = self.fileName[0]
            self.GetAndSetImg(self.fileName[0])
        

    

    def GetAndSetImg(self,file_name):
        try:        
            self.matImg= cv.imread(file_name[0])
            self.image_path=file_name[0]
            self.image_paths_len=3
            self.SetSystemSearchedFlag(True)
            matRGBImg=cv.cvtColor(self.matImg, cv.COLOR_BGR2RGB)
            Qimg = gui.QImage(matRGBImg.data, matRGBImg.shape[1], matRGBImg.shape[0], gui.QImage.Format_RGB888)
            pixelImg = gui.QPixmap.fromImage(Qimg)
            self.lblOpenImg.setPixmap(pixelImg)
        except Exception as ex:
            logData("Exception on "+ str(ex))
            self.txtSystemStatus.append("Exception on "+ str(ex))
            
    def SetSystemSearchedFlag(self,flag):
        self.isSystemSearched=flag


                

def moveAFile(src,dst):
    try:
       shutil.move(src,dst)
    except Exception as ex:
        logData("Exception on " +str(ex))

def organizeFile(src, ext,prefix):
    try:
        _src = src
        _ext = ext
        #endsWithNumber =  re.compile(r'(\d+)'+(re.escape(_ext))+'$')
        fileCounter=0
        for i , filename in enumerate(os.listdir(_src)):
            fileCounter=i
        fileCounter=int(math.floor(math.log10(fileCounter))+1)  
        logData("file Counter ["+ str(fileCounter)+"]")
        if fileCounter <= 3:
            fileCounter=3    
        for i , filename in enumerate(os.listdir(_src)):
            if filename.endswith(_ext) or filename.endswith(".jpeg"):
                src=_src+ prefix + str(i).zfill(fileCounter)+".jpg"
                if (_src+filename) != src:
                    os.rename(_src+filename, src)
    except Exception as ex:
        logData("Exception on "+ str(ex))

def removeAFile(src):
    for filename in os.listdir(src):
        file_path = os.path.join(src, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logData('Failed to delete %s. Reason: %s' % (file_path, e))   


class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()

        openButton = QPushButton("Open Video")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(btnSize)
        openButton.setFont(QFont("Noto Sans", 8))
        openButton.setIcon(QIcon.fromTheme("document-open", QIcon("D:/_Qt/img/open.png")))
        openButton.clicked.connect(self.abrir)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

    def abrir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "select the video",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            print(fileName)
            os.system("python videoSearch.py "+fileName +" static/video/ 30")
            self.statusBar.showMessage(fileName)
            self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())
           

def logData(data):
    print  ("["+ str(datetime.datetime.now())+"]  " + data)
    
def main():
    cv.__version__
    app=qwd.QApplication(sys.argv)
    ## main gui
    ex=firstGui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()