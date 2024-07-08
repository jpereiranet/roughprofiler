import os
import sys
import time
import pyqtgraph as pg
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QProgressBar, QSplashScreen
from PyQt5.QtGui import QPixmap
from main import Ui_RoughProfiler2
from developraw import DevelopImages
import math
import os
import subprocess
import sys
import exifread
from app_paths import DefinePathsClass
import configparser
from proof_file import CreateProofImage
import json
import glob

class HomeUI(QtWidgets.QDialog):

    def __init__(self, parent=None):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        if os.path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.pathArgyllExecutables = self.config['APPS']['ARGYLL']
            self.pathDcamprofExecutables = self.config['APPS']['DCAMPROF']
            self.lay_w = int(self.config['LAYOUT']['LAY_W'])
            self.lay_h = int(self.config['LAYOUT']['LAY_H'])
            self.pad_roi = int(self.config['LAYOUT']['PAD_ROI'])
            self.copyright = self.config['OTHERS']['COPYRIGHT']


            self.ArgyllRes = json.loads(self.config.get('PARAMS', 'ARGYLLRES'))
            self.ArgyllAlgoritm = json.loads(self.config.get('PARAMS', 'ARGYLLALGORITM'))
            self.ArgyllUParam = json.loads(self.config.get('PARAMS', 'ARGYLLUPARAM'))
            self.Targets = json.loads(self.config.get('PARAMS', 'TARGETS'))

        else:
            print("error load configuration")


        #self.inputImage = "DSC_4453a.TIF"

        super(HomeUI, self).__init__(parent)
        self.ui = Ui_RoughProfiler2()
        self.ui.setupUi(self)

        #self.ui.verticalLayout.addWidget()
        self.ui.TargetType.addItems( self.Targets.keys() )
        self.ui.ArgyllRes.addItems (self.ArgyllRes.keys() )
        self.ui.ArgyllAlgoritm.addItems( self.ArgyllAlgoritm.keys() )
        self.ui.ArgyllUparam.addItems( self.ArgyllUParam.keys() )
        self.ui.tabWidget_2.setTabEnabled(2, False)
        self.ui.tabWidget_2.setTabEnabled(1, False)
        self.ui.tabWidget_2.setTabEnabled(0, False)
        self.ui.tabWidget_2.setCurrentIndex(0)
        #--- open imagen
        self.ui.ExecuteReadImage.clicked.connect( self.readImage )
        self.ui.textEdit.setReadOnly(True)
        self.ui.OpenImage.clicked.connect( self.openTestImage )
        self.ui.OpenImage.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('picture_64px.png')))
        self.ui.OpenImage.setIconSize(QtCore.QSize(30, 30))
        # --- Load CGATS
        self.ui.LoadCGATS.setEnabled(False)
        self.ui.LoadCGATS.clicked.connect( self.openCGATS )
        self.ui.LoadCGATS.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('document_64px.png')))
        self.ui.LoadCGATS.setIconSize(QtCore.QSize(45, 45))
        # --- Scanin
        self.ui.ExecuteReadImage.setEnabled(False)
        self.ui.ExecuteReadImage.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('scaning_64px.png')))
        self.ui.ExecuteReadImage.setIconSize(QtCore.QSize(45, 45))
        # --- Execute task
        self.ui.ExecuteTask.setEnabled(False)
        self.ui.ExecuteTask.clicked.connect(self.executeProcess)
        self.ui.ExecuteTask.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('execute_64px.png')))
        self.ui.ExecuteTask.setIconSize(QtCore.QSize(45, 45))
        # --- install profile
        self.ui.InstallProfile.setEnabled(False)
        self.ui.InstallProfile.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('execute_64px.png')))
        self.ui.InstallProfile.setIconSize(QtCore.QSize(45, 45))
        # --- Create Proof image
        self.ui.createProofImage.setEnabled(False)
        self.ui.createProofImage.clicked.connect(self.createdProofimage)
        self.ui.createProofImage.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('execute_64px.png')))
        self.ui.createProofImage.setIconSize(QtCore.QSize(45, 45))

        self.ui.CopyRightText.setText(self.copyright)
        self.ui.radioButton.setChecked(True)
        self.ui.tabWidget.setTabEnabled(1, False)

        self.ui.DcamprofDCP.setChecked(True)
        self.ui.DcamprofICC.setChecked(False)
        self.ui.DcamprofDCP.clicked.connect(self.dcamprofDCPRadio)
        self.ui.DcamprofICC.clicked.connect(self.dcamprofICCRadio)


        self.ui.radioButton.clicked.connect(self.showArgyllWorkflow)
        self.ui.radioButton_2.clicked.connect(self.showDcamprofWorkflow)

        self.ui.ARgyllUslicer.setEnabled(False)

        self.ui.ARgyllUslicer.valueChanged[int].connect(self.updateSliderLabel)

        self.ui.ArgyllEmphasisSlider.valueChanged[int].connect(self.updateSliderLabelEmphasis)

        self.ui.ArgyllUparam.currentTextChanged.connect(self.enableSlider)

        self.ui.FileNameValue.setText("nada")

        #ArgyllEmphasisSlider

        #self.ui.DcamprofIlluminant
        #self.comboBox.currentIndexChanged.connect(self.update_chart)

    def updateSliderLabel(self):
        valor = self.ui.ARgyllUslicer.value()
        valor = round(valor * 0.1,1)
        self.ui.ArgyllUscale.setText( str(valor) )

    def updateSliderLabelEmphasis(self):
        valor = self.ui.ArgyllEmphasisSlider.value()
        valor = round(valor * 0.1,1) + 1
        self.ui.ArgyllGridEmphasis.setText( str(valor) )

    def enableSlider(self):
        if self.ui.ArgyllUparam.currentIndex() == 4:  # if is "custom"
            self.ui.ARgyllUslicer.setEnabled(True)


    def showArgyllWorkflow(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.setTabEnabled(1,False)
        self.ui.tabWidget.setTabEnabled(0, True)
        self.ui.radioButton.setChecked(True)
        self.ui.radioButton_2.setChecked(False)

    def showDcamprofWorkflow(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.tabWidget.setTabEnabled(1, True)
        self.ui.radioButton.setChecked(False)
        self.ui.radioButton_2.setChecked(True)

    def dcamprofICCRadio(self):
        self.ui.DcamprofDCP.setChecked(False)
        self.ui.DcamprofICC.setChecked(True)


    def dcamprofDCPRadio(self):
        self.ui.DcamprofDCP.setChecked(True)
        self.ui.DcamprofICC.setChecked(False)

    def getMetadata(self, img):

        im = open(img, 'rb')
        metadata = exifread.process_file(im)
        if str(metadata['Image Make']) != "":
            manufacturer = str(metadata['Image Make'])
        else:
            manufacturer = "Manufacturer"

        if str(metadata['Image Model']) != "":
            model = str(metadata['Image Model'])
        else:
            model = "Model"

        self.ui.ManufacturerText.setText(manufacturer)
        self.ui.ModelText.setText(model)

        filename = model+".icc"
        filename = self.createICCFileName(filename.replace(" ","_"))

        self.ui.FileNameText.setText(filename.replace(" ","_")+".icc")
        self.ui.DestText.setText(filename.replace("_"," "))



    def openTestImage(self):
        '''
        Open test image dialog
        :return:
        '''

        path = "/Users/jpereira/Python/roughprofiler2/test"
        qfd = QtWidgets.QFileDialog()
        paths = [str(file_n) for file_n in list(
            QtWidgets.QFileDialog.getOpenFileNames(qfd, "Select files", path,
                                                   filter='Images (*.png *.tif *.tiff  *.jpg *.jpeg *.dng *.nef)'
                                                   )[0])]
        #print(paths)
        self.inputImage = paths[0]
        self.ui.FileNameValue.setText(os.path.basename(paths[0]))

        if os.path.isfile(paths[0]):

            self.isRaw = False
            self.CEGATS_path = False
            self.ui.tabWidget_2.setTabEnabled(0, True)
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.ui.ExecuteReadImage.setEnabled(True)
            self.ui.LoadCGATS.setEnabled(True)
            self.ui.createProofImage.setEnabled(True)
            self.inputImage = paths[0]
            self.filename = os.path.splitext(os.path.basename(self.inputImage))[0]
            self.tempFolder = os.path.join(os.path.dirname(paths[0]), self.filename)
            self.ti3 = os.path.join(self.tempFolder, self.filename + ".ti3")
            self.diag = os.path.join(self.tempFolder, self.filename + "_diag.tiff")
            self.getMetadata(paths[0])
            self.outputICCfilename = os.path.join(self.tempFolder, self.ui.FileNameText.text())
            self.checkIfRawFile()
            self.loadImage()
            self.checkTempFolderContents()

    def checkIfRawFile(self):
        '''
        if is a raw file create a thumbnail with rawpy
        :return:
        '''
        rawExt = [".DNG",".dng", ".NEF", ".nef"]
        if os.path.splitext(os.path.basename(self.inputImage))[1] in rawExt:
            self.rawinputfile = self.inputImage
            path = os.path.join(self.tempFolder, "thumb_" + self.filename + ".tiff")
            if not os.path.isfile(path):
                self.createTempFolder()
                #rgbImage = DevelopImages.raw_get_thumbnail(self.inputImage)
                rgbImage = DevelopImages.raw_gamma_develop(self.inputImage)

                cv2.imwrite(path, rgbImage)
            if os.path.isfile(path):
                self.inputImage = path
                self.isRaw = True

    def checkTempFolderContents(self):
        '''
        if exist a temp folder with files, load it
        :return:
        '''

        if os.path.isdir(self.tempFolder):
            if os.path.isfile(self.ti3):
                self.ui.ExecuteTask.setEnabled(True)

            if os.path.isfile(self.diag):
                self.loadDiag()
                self.ui.tabWidget_2.setTabEnabled(1, True)


    def openCGATS(self):
        '''
        Open reference file in CEGATS format
        :return:
        '''
        qfd = QtWidgets.QFileDialog()
        path = "/Users/jpereira/Python/roughprofiler2/test"

        filter = "Images (*.txt *.cie)"
        title = "GET CGATS"
        fname = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
        # print( fname)
        if os.path.isfile(fname):
            self.CEGATS_path = str(fname)
            self.ui.ReferenceNameValue.setText(os.path.basename(self.CEGATS_path))

    def executeProcess(self):
        '''
        Execute ArgyllCMS o Dcamprof workflows
        :return:
        '''
        if self.ui.radioButton.isChecked():
            self.runColprof()

        if self.ui.radioButton_2.isChecked():
            if self.ui.DcamprofDCP.isChecked():
                self.runDcamprof()
            if self.ui.DcamprofICC.isChecked():
                self.runDcamprofICC()


    def runDcamprof(self):

        target =  self.Targets[list( self.Targets)[self.ui.TargetType.currentIndex()]]
        jsonInProfile = os.path.join(self.pathRepo,target[2] )
        executables = os.path.join(self.pathDcamprofExecutables, "dcamprof")
        jsonOutProfile = os.path.join( self.tempFolder, self.filename+".json" )
        dcpFile = os.path.join( self.tempFolder, self.filename+".dcp" )

        # make-profile -g cc24-layout.json rawfile.ti3 profile.json
        cmd = [executables, "make-profile", "-g",jsonInProfile, self.ti3, jsonOutProfile  ]
        print(cmd)
        self.executeTool(cmd, "Dcamprof make-profile", "dcamprof")
        cmd = [executables, "make-dcp", "-n", "Nikon", "-d", "mi profile", "-t", "acr",jsonOutProfile,  dcpFile]
        print(cmd)
        self.executeTool(cmd, "Dcamprof make-dcp", "dcamprof")
        #dcamprof make-dcp -n "Camera manufacturer and model" -d "My Profile" -t acr profile.json profile.dcp


    def runDcamprofICC(self):

        #dcamprof make-profile -g cc24-layout.json new-target.ti3 profile.json
        #dcamprof make-icc -n "Camera manufacturer and model" -f target.tif -t acr profile.json profile.icc

        target =  self.Targets[list( self.Targets)[self.ui.TargetType.currentIndex()]]
        jsonInProfile = os.path.join(self.pathRepo,target[2] )
        executables = os.path.join(self.pathDcamprofExecutables, "dcamprof")
        jsonOutProfile = os.path.join( self.tempFolder, self.filename+".json" )
        iccFile = os.path.join( self.tempFolder, self.filename+".icc" )

        cmd = [executables, "make-profile", "-g", jsonInProfile, self.ti3, jsonOutProfile  ]

        cmd = [executables, "make-icc", "-n", "Nikon", "-d", "mi profile", "-t", "acr",jsonOutProfile,  iccFile]




    def runColprof(self):
        '''
        run ArgyllCMS Colprof
        :return:
        '''

        manufacturer = self.ui.ManufacturerText.text()
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        copyright = self.ui.CopyRightText.text()
        argyllAlgoritm = self.ArgyllAlgoritm[ list(self.ArgyllAlgoritm)[self.ui.ArgyllAlgoritm.currentIndex()] ]
        argyllRes = self.ArgyllRes[list(self.ArgyllRes)[self.ui.ArgyllRes.currentIndex()]]
        argyllUParam = self.ArgyllUParam[list(self.ArgyllUParam)[self.ui.ArgyllUparam.currentIndex()]]

        if self.ui.ArgyllUparam.currentIndex() == 4: # if is "custom"
            valor = self.ui.ARgyllUslicer.value()
            argyllUParam = "-U"+ str(round(valor * 0.1,1) * 1)

        emphasis = self.ui.ArgyllEmphasisSlider.value()
        emphasis = "-V"+ str(round(emphasis * 0.1, 1) + 1)

        executable = os.path.join(self.pathArgyllExecutables, "colprof")

        cmd = [executable, "-v","-a", argyllAlgoritm,"-q",argyllRes, emphasis, argyllUParam ,"-O",self.outputICCfilename,"-A",manufacturer, "-M", model, "-D",description,"-C", copyright, os.path.splitext(self.ti3)[0]   ]
        print(cmd)
        self.executeTool(cmd, "COLPROF", "argyll")

        if os.path.isfile(self.outputICCfilename):
            self.ui.createProofImage.setEnabled(True)
            self.ui.InstallProfile.setEnabled(True)
            filename = self.createICCFileName(os.path.basename( self.outputICCfilename ) )
            self.ui.FileNameText.setText(filename.replace(" ","_")+".icc")
            self.ui.DestText.setText(filename.replace("_", " ") )

    def createdProofimage(self):

        CreateProofImage(self.inputImage, self.outputICCfilename, self.ui, self.tempFolder)

    def createTempFolder(self):
        '''
        Create de folder to store all temporary files .ti3, .icc, thumbs, etc
        :return:
        '''

        if not os.path.isdir(self.tempFolder):
            os.mkdir(self.tempFolder)

    def checkCoordinatesInside(self):
        '''
        if coordinates is bigger than image infinite loop may apear in scanin
        coordinates are (w,h) and cv2 shape are (h,w)
        :return: bool
        '''
        if self.isRaw:
            size = self.linealImageSize
        else:
            size = self.gammaImageSize

        for i in self.coodinates:
            if i[1] > size[0]:
                return False
            elif i[0] > size[1]:
                return False
        return True

    def createLinearImage(self):
        '''
        Create a linear RGB image with gamma 1 from raw file
        :return:
        '''

        path = os.path.join(self.tempFolder, "lineal_" + self.filename + ".tiff")
        if not os.path.isfile(path):
            self.ui.tabWidget_2.setCurrentIndex(2)
            self.ui.tabWidget_2.setTabEnabled(2, True)
            self.ui.textEdit.clear()
            self.ui.textEdit.insertPlainText("Raw processing wait a moment\n")
            QApplication.processEvents()
            linealImage = DevelopImages.raw_lineal_develop(self.rawinputfile)
            cv2.imwrite(path, linealImage)

        if os.path.isfile(path):
            self.inputImage = path
            self.linealImageSize = cv2.imread(path).shape
            self.gamma = "-G1.0"
            return True
        else:
            print("No linear image from raw was created")
            return False


    def readImage(self):
        '''
        Read image with ArgyllCMS scanin
        :return:
        '''

        self.createTempFolder()
        self.gamma = "-G2.2"

        if self.isRaw:
            self.createLinearImage()

        if self.checkCoordinatesInside():

            targetKey = list(params.targets)[ self.ui.TargetType.currentIndex()]
            target = params.targets[targetKey]
            #scanin -v -p -dipn rawfile.tif ColorChecker.cht cc24_ref.cie
            executable = os.path.join( self.pathArgyllExecutables, "scanin")
            #recogfile = os.path.join( self.pathRepo, target[1])
            #reference = os.path.join(self.pathRepo, target[0])
            if not self.CEGATS_path:
                reference = DefinePathsClass.create_reference_paths( target[0] )
            else:
                reference = self.CEGATS_path

            recogfile = DefinePathsClass.create_reference_paths(target[1])
            if not os.path.isfile(recogfile):
                print("error no se encuenta")
            else:

                #coordinate to string
                res = []
                for i in self.coodinates:
                    for j in i:
                     res.append( str(round(j,2)) )
                coor = ",".join(res)

                cmd = [executable, "-v2", "-p","-dipn", self.gamma, "-F", coor, "-O", self.ti3,  self.inputImage, recogfile, reference, self.diag ]
                print(" ".join(cmd) )
                self.executeTool(cmd, "SCANIN", "argyll")

                if os.path.isfile(self.ti3):
                    #enable ICC/DCP buton
                    self.ui.ExecuteTask.setEnabled(True)
                if os.path.isfile(self.diag):
                    #load diag image
                    self.loadDiag()
                    self.ui.tabWidget_2.setTabEnabled(1, True)
                    self.ui.tabWidget_2.setCurrentIndex(1)
        else:
            print("coordenadas mayores que imagen!")


    def executeTool(self, cmd, toolName, workflow):
        '''
        Execute binary files
        :param cmd: list of params
        :param toolName: string with name of tool for informative log
        :return:
        '''

        self.ui.tabWidget_2.setCurrentIndex(2)
        self.ui.tabWidget_2.setTabEnabled(2, True)
        self.ui.textEdit.clear()
        self.ui.textEdit.insertPlainText("---- "+toolName+"-----\n")
        QApplication.processEvents()

        cmd =  list(filter(None, cmd))
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, bufsize=1)

        if workflow == "dcamprof":
            output = p.stderr.readline
        elif workflow == "argyll":
            output = p.stdout.readline

        for line in iter(output, b''):
            self.ui.textEdit.insertPlainText(line.decode('utf-8'))
            self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
            QApplication.processEvents()
        p.stdout.close()
        p.wait()

    def loadDiag(self):
        '''
        Load the diag tiff files result from ArgyllCMS scanin
        :return:
        '''

        if os.path.isfile( self.diag ):

            #clean widgets before
            for i in reversed(range(self.ui.verticalLayout_2.count())):
                self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)

            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
            graphicsView.setObjectName("graphicsView")
            v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
            v2a.setMouseEnabled(x=False, y=False)
            v2a.setLimits(xMin=0, xMax=self.lay_w)
            v2a.setAspectLocked()
            v2a.disableAutoRange('xy')

            image_data = cv2.imread(self.diag)
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
            image_data = image_data.astype(np.uint16)

            image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)
            #image apear flip in viewBox ¿?
            image_data = cv2.flip(image_data, 0)
            imageitem = pg.ImageItem(image_data, axisOrder='row-major')
            v2a.addItem(imageitem)
            v2a.autoRange()

            self.ui.verticalLayout_2.addWidget(graphicsView)



    def loadImage(self ):
        '''
        Load proof image on main layout, first tab
        :return:
        '''

        #clean widgets before
        for i in reversed(range(self.ui.verticalLayout.count())):
            self.ui.verticalLayout.itemAt(i).widget().setParent(None)

        graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
        graphicsView.setObjectName("graphicsView")
        v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
        v2a.setMouseEnabled(x=False, y=False)
        v2a.setLimits(xMin=0, xMax=self.lay_w)
        v2a.setAspectLocked()
        v2a.invertY(True)
        v2a.disableAutoRange('xy')

        image_data = cv2.imread( self.inputImage )
        self.gammaImageSize = image_data.shape
        image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        image_data = image_data.astype(np.uint16)
        image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)

        imageitem = pg.ImageItem(image_data, axisOrder='row-major')

        v2a.addItem(imageitem)
        v2a.addItem( self.createROI() ) #load ROI
        v2a.autoRange()

        self.ui.verticalLayout.addWidget(graphicsView)


    def createROI(self):
        '''
        Create Region Of Interest
        :return:
        '''

        centro = [self.lay_w/2, self.lay_h/2]
        ratio = self.lay_w / self.lay_h
        top_left = [ centro[0] - self.pad_roi*ratio/2, centro[1] - self.pad_roi/2 ]

        my_roi = pg.ROI(top_left, [self.pad_roi*ratio, self.pad_roi], pen=pg.mkPen(width=4.5, color='r'))

        my_roi.addScaleHandle([1, 1], [0, 0], lockAspect=False)
        my_roi.addScaleHandle([0, 0], [1, 1], lockAspect=False)
        my_roi.addScaleHandle([1, 0], [0, 1], lockAspect=False)
        my_roi.addScaleHandle([0, 1], [1, 0], lockAspect=False)
        my_roi.addRotateHandle([1, 0.5], [0.5, 0.5])
        my_roi.sigRegionChangeFinished.connect(lambda roi: self.createCoordinates( roi) )

        return my_roi

    '''
    def roiMove(self, roi):
        """Print the coordinates of the ROI."""
      # polyline.sigRegionChanged.connect(self.roiMove(polyline))
        pts = roi.getSceneHandlePositions()
        print([roi.mapSceneToParent(pt[1]) for pt in pts])
    '''
    '''
    def roi_changed(self, roi):

        #hh = roi.getHandles()
        
        #Handles = roi.getLocalHandlePositions()  # Get list of handles
        #Handles2 = roi.getSceneHandlePositions()

        #for h in Handles:
            #print(h[1])
            #h["item"].sigClicked.connect(self.sigRegionChangeStarted.emit)
            #position = h[1]
            #print(f'point = ({position.x():.4f},{position.y():.4f})')
    '''

    def rotate_via_numpy(self, xy, degrees):
        '''
        Rotate ROI after scale
        :param xy:
        :param degrees:
        :return:
        '''
        #https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302

        radians = math.radians(degrees)
        x, y = xy
        c, s = np.cos(radians), np.sin(radians)
        j = np.matrix([[c, s], [-s, c]])
        m = np.dot(j, [x, y])

        return float(m.T[0]), float(m.T[1])

    def createCoordinates(self, roi):
        '''
        Get coordinates from ROI
        format (Width, Height)
        :param roi:
        :return:
        '''
        state = roi.getState()
        x = state['pos'][0] * self.factor
        y = state['pos'][1] * self.factor
        w = state['size'][0] * self.factor
        h = state['size'][1] * self.factor
        #corrige la rotación sino la hace al contrario ¿?
        angle = state['angle'] *  -1

        top_left = self.rotate_via_numpy( (x, y), angle)
        top_right = self.rotate_via_numpy( (w + x,   y), angle)
        bottom_right = self.rotate_via_numpy( (w+x , h+y), angle)
        bottom_left = self.rotate_via_numpy( (x, h+y), angle)

        self.coodinates = [top_left, top_right, bottom_right, bottom_left ]
        #print(self.coodinates)

    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        '''
        Resize image to fit inside layout
        :param image:
        :param width:
        :param height:
        :param inter:
        :return:
        '''

        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)

        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv2.resize(image, dim, interpolation = inter)

        (h1, w1) = resized.shape[:2]
        factor = w/w1

        return resized, factor

    def createICCFileName(self, filen):

        os.chdir(self.tempFolder)
        files = glob.glob("*.icc")
        files.sort(key=os.path.getmtime)

        if len(files) > 0:
            last = files[-1]
            name_orig, ext_orig = os.path.splitext(last)
            arr = name_orig.split("_")
            lastSection = arr[-1]

            if "VE" in lastSection: #revisar esto que no funciona
                lastItem = lastSection.replace("VE", "")
                if lastItem.isdigit():
                    newnumber = "VE" + str(int(lastItem) + 1)
            else:
                newnumber = "VE1"

            arr.pop()
            arr.append(str(newnumber))
            filen = "_".join(arr)


        filen = os.path.splitext(filen)[0]

        return filen



if __name__ == '__main__':

    app = QApplication(sys.argv)

    main = HomeUI()
    main.show()
    sys.exit(app.exec_())

