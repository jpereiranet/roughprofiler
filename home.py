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

import math
from params import params
import os
import subprocess
import sys




class HomeUI(QtWidgets.QDialog):

    def __init__(self, parent=None):

        self.lay_w = 570
        self.lay_h = 400
        self.pad_roi = 100

        self.pathArgyllExecutables = "/Users/jpereira/Python/imageProfiler/programs/argyll"
        self.pathDcamprofExecutables = "/Users/jpereira/Python/imageProfiler/programs/dcamprof/"
        self.pathRepo = "/Users/jpereira/Python/imageProfiler/resources/"
        #self.dcrawExecutable = "/usr/local/Cellar/dcraw/9.28.0/bin/dcraw"

        self.par = params()
        #self.inputImage = "DSC_4453a.TIF"

        super(HomeUI, self).__init__(parent)
        self.ui = Ui_RoughProfiler2()
        self.ui.setupUi(self)
        #self.ui.verticalLayout.addWidget()
        self.ui.TargetType.addItems(self.par.targets.keys())
        self.ui.ArgyllRes.addItems(self.par.ArgyllResolutions.keys())
        self.ui.ArgyllAlgoritm.addItems(self.par.ArgyllAlgoritms.keys())
        self.ui.ArgyllUparam.addItems(self.par.ArgyllUparam.keys())
        self.ui.tabWidget_2.setTabEnabled(2, False)
        self.ui.tabWidget_2.setTabEnabled(1, False)
        self.ui.tabWidget_2.setTabEnabled(0, False)
        self.ui.tabWidget_2.setCurrentIndex(0)

        self.ui.ExecuteReadImage.clicked.connect( self.readImage )
        self.ui.textEdit.setReadOnly(True)
        self.ui.OpenImage.clicked.connect( self.openTestImage )
        self.ui.LoadCGATS.clicked.connect( self.openCGATS )
        self.ui.radioButton.setChecked(True)
        self.ui.tabWidget.setTabEnabled(1, False)

        self.ui.ExecuteTask.clicked.connect(self.executeProcess)
        self.ui.radioButton.clicked.connect(self.showArgyllWorkflow)
        self.ui.radioButton_2.clicked.connect(self.showDcamprofWorkflow)

        self.ui.ARgyllUslicer.setEnabled(False)

        self.ui.ARgyllUslicer.valueChanged[int].connect(self.updateSliderLabel)

        self.ui.ArgyllEmphasisSlider.valueChanged[int].connect(self.updateSliderLabelEmphasis)

        self.ui.ArgyllUparam.currentTextChanged.connect(self.enableSlider)

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

    def showDcamprofWorkflow(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.tabWidget.setTabEnabled(1, True)


    def openTestImage(self):

        path = "/Users/jpereira/Python/imageProfiler/"
        qfd = QtWidgets.QFileDialog()
        paths = [str(file_n) for file_n in list(
            QtWidgets.QFileDialog.getOpenFileNames(qfd, "Select files", path,
                                                   filter='Images (*.png *.tif *.tiff  *.jpg *.jpeg)'
                                                   )[0])]
        print(paths)
        self.inputImage = paths[0]

        if os.path.isfile(paths[0]):
            self.ui.tabWidget_2.setTabEnabled(0, True)
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.inputImage = paths[0]
            os.path.splitext(os.path.basename(self.inputImage))[0]
            self.ui.FileNameValue.setText(os.path.basename(self.inputImage))
            self.loadImage()



    def openCGATS(self):

        qfd = QtWidgets.QFileDialog()
        path = "/Users/jpereira/Python/imageProfiler/"

        filter = "Images (*.txt *.cie)"
        title = "GET CGATS"
        fname = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
        # print( fname)
        if os.path.isfile(fname):
            self.CEGATS_path = str(fname)
            self.ui.ReferenceNameValue.setText(os.path.basename(self.CEGATS_path))

    def executeProcess(self):

        if self.ui.radioButton.isChecked():
            self.runColprof()

        if self.ui.radioButton_2.isChecked():
            self.runDcamprof()


    def runDcamprof(self):
        print("helooooooooooooo")


    def runColprof(self):

        manufacturer = self.ui.ManufacturerText.text()
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        copyright = self.ui.CopyRightText.text()
        outputfilename = self.ui.FileNameText.text()
        argyllAlgoritm = self.par.ArgyllAlgoritms[ list(self.par.ArgyllAlgoritms)[ self.ui.ArgyllAlgoritm.currentIndex()] ]
        argyllRes = self.par.ArgyllResolutions[list(self.par.ArgyllResolutions)[self.ui.ArgyllRes.currentIndex()]]
        argyllUParam = self.par.ArgyllUparam[list(self.par.ArgyllUparam)[self.ui.ArgyllUparam.currentIndex()]]

        if self.ui.ArgyllUparam.currentIndex() == 4: # if is "custom"
            valor = self.ui.ARgyllUslicer.value()
            argyllUParam = "-U"+ str(round(valor * 0.1,1) * 1)

        emphasis = self.ui.ArgyllEmphasisSlider.value()
        emphasis = "-V"+ str(round(emphasis * 0.1, 1) + 1)

        executable = os.path.join(self.pathArgyllExecutables, "colprof")

        cmd = [executable, "-v","-a", argyllAlgoritm,"-q",emphasis, argyllRes, argyllUParam ,"-O",outputfilename,"-A",manufacturer, "-M", model, "-D",description,"-C", copyright, "DSC_4453a"   ]
        print(cmd)
        self.executeTool(cmd, "COLPROF")

    def readImage(self):

        targetKey = list(self.par.targets)[ self.ui.TargetType.currentIndex()]
        target = self.par.targets[targetKey]
        #scanin -v -p -dipn rawfile.tif ColorChecker.cht cc24_ref.cie
        executable = os.path.join( self.pathArgyllExecutables, "scanin")
        recogfile = os.path.join( self.pathRepo, target[1])
        reference = os.path.join(self.pathRepo, target[0])

        coordinates = self.coodinates
        #coordinate to string
        res = []
        for i in coordinates:
            for j in i:
             res.append( str(round(j,2)) )
        coor = ",".join(res)

        cmd = [executable, "-v2", "-p","-dipn","-F", coor, self.inputImage, recogfile, reference ]

        self.executeTool(cmd, "SCANIN")

        self.loadDiag()
        self.ui.tabWidget_2.setTabEnabled(1, True)
        self.ui.tabWidget_2.setCurrentIndex(1)


    def executeTool(self, cmd, toolName):

        self.ui.tabWidget_2.setCurrentIndex(2)
        self.ui.tabWidget_2.setTabEnabled(2, True)
        self.ui.textEdit.clear()
        self.ui.textEdit.insertPlainText("---- "+toolName+"-----\n")
        QApplication.processEvents()

        cmd =  list(filter(None, cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, b''):
            self.ui.textEdit.insertPlainText(line.decode('utf-8'))
            self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
            QApplication.processEvents()
        p.stdout.close()
        p.wait()

    def loadDiag(self):

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

        image_data = cv2.imread("diag.tif")
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

        graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
        graphicsView.setObjectName("graphicsView")
        v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
        v2a.setMouseEnabled(x=False, y=False)
        v2a.setLimits(xMin=0, xMax=self.lay_w)
        v2a.setAspectLocked()
        v2a.invertY(True)
        v2a.disableAutoRange('xy')

        image_data = cv2.imread( self.inputImage )
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
        polyline = GraphPolyLine(
            [[0, 0], [0, 50], [50, 50], [50, 0]],
            closed=True,
            pen=pg.mkPen('b', width=5),
            resizable=True,
            maxBounds=QtCore.QRectF(0, 0, 300, 200)
        )
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
        """Use numpy to build a rotation matrix and take the dot product."""
        #https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302

        radians = math.radians(degrees)
        x, y = xy
        c, s = np.cos(radians), np.sin(radians)
        j = np.matrix([[c, s], [-s, c]])
        m = np.dot(j, [x, y])

        return float(m.T[0]), float(m.T[1])

    def createCoordinates(self, roi):
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



if __name__ == '__main__':

    app = QApplication(sys.argv)

    main = HomeUI()
    main.show()
    sys.exit(app.exec_())

