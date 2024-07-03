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
from handle import GraphPolyLine
import math
from params import params
import os
from executables import executables



class HomeUI(QtWidgets.QDialog):

    def __init__(self, parent=None):

        self.lay_w = 570
        self.lay_h = 400
        self.pad_roi = 100

        self.pathArgyllExecutables = "/Users/jpereira/Python/imageProfiler/programs/argyll"
        self.pathDcamprofExecutables = "/Users/jpereira/Python/imageProfiler/programs/dcamprof/"
        self.pathRepo = "/Users/jpereira/Python/imageProfiler/resources/"

        self.par = params()
        self.inputImage = "DSC_4453a.TIF"

        super(HomeUI, self).__init__(parent)
        self.ui = Ui_RoughProfiler2()
        self.ui.setupUi(self)
        self.ui.verticalLayout.addWidget( self.loadImage())
        self.ui.TargetType.addItems(self.par.targets.keys())
        self.ui.ArgyllRes.addItems(self.par.ArgyllResolutions.keys())
        self.ui.ArgyllAlgoritm.addItems(self.par.ArgyllAlgoritms.keys())
        self.ui.ArgyllUparam.addItems(self.par.ArgyllUparam.keys())
        self.ui.ExecuteTask.clicked.connect( self.createTerminal )
        self.ui.ExecuteReadImage.clicked.connect( self.readImage )
        #self.ui.DcamprofIlluminant

        #self.comboBox.currentIndexChanged.connect(self.update_chart)

    def createTerminal(self):

        '''
        manufacturer = self.ui.ManufacturerText.text()
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        copyright = self.ui.CopyRightText.text()
        outputfilename = self.ui.FileNameText.text()
        targets = self.ui.TargetType.currentIndex()
        argyllAlgoritm = self.ui.ArgyllAlgoritm.currentIndex()
        argyllRes = self.ui.ArgyllRes.currentIndex()
        argyllParam = self.ui.ArgyllUparam.currentIndex()
        '''


        return "XXX"

    def readImage(self):

        targetKey = list(self.par.targets)[ self.ui.TargetType.currentIndex()]
        target = self.par.targets[targetKey]
        #scanin -v -p -dipn rawfile.tif ColorChecker.cht cc24_ref.cie
        executable = os.path.join( self.pathArgyllExecutables, "scanin")
        recogfile = os.path.join( self.pathRepo, target[1])
        reference = os.path.join(self.pathRepo, target[0])

        coordinates = self.coodinates

        res = []
        for i in coordinates:
            for j in i:
             res.append( str(round(j,2)) )

        coor = ",".join(res)

        cmd = [executable, "-v2", "-p","-dipn","-F", coor, self.inputImage, recogfile, reference ]

        exe = executables()
        output = exe.runScanin(cmd)
        #print(cmd)
        #print( output[0].decode('utf-8') )

        self.ui.textEdit.append( output[0].decode('utf-8') )
        self.loadDiag()
        self.ui.tabWidget_2.setCurrentIndex(1)
        #return terminal

    def loadDiag(self):

        graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
        graphicsView.setObjectName("graphicsView")
        v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
        v2a.setMouseEnabled(x=False, y=False)
        v2a.setLimits(xMin=0, xMax=self.lay_w)
        v2a.setAspectLocked()

        image_data = cv2.imread("diag.tif")
        image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        image_data = image_data.astype(np.uint16)

        image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)
        #image_data = cv2.rotate(image_data, cv2.ROTATE_180)
        imageitem = pg.ImageItem(image_data, axisOrder='row-major')
        v2a.addItem(imageitem)

        v2a.disableAutoRange('xy')
        v2a.autoRange()

        self.ui.verticalLayout_2.addWidget(graphicsView)



    def loadImage(self ):

        graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
        graphicsView.setObjectName("graphicsView")
        v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
        v2a.setMouseEnabled(x=False, y=False)
        v2a.setLimits(xMin=0, xMax=self.lay_w)
        v2a.setAspectLocked()

        image_data = cv2.imread( self.inputImage )
        image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        image_data = image_data.astype(np.uint16)

        image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)
        imageitem = pg.ImageItem(image_data, axisOrder='row-major')
        v2a.addItem(imageitem)

        v2a.addItem( self.createROI() ) #load ROI
        v2a.invertY(True)
        v2a.disableAutoRange('xy')
        v2a.autoRange()

        return graphicsView


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
        angle = state['angle']

        top_left = self.rotate_via_numpy( (x, y), angle)
        top_right = self.rotate_via_numpy( (w + x,   y), angle)
        bottom_right = self.rotate_via_numpy( (w+x , h+y), angle)
        bottom_left = self.rotate_via_numpy( (x, h+y), angle)

        self.coodinates = [top_left, top_right, bottom_right, bottom_left ]
        print(self.coodinates)

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

