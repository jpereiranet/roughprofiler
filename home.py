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
from warning_class import AppWarningsClass
import shutil
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from color import ColorProof
from confclass import ConfIni


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
            #self.copyright = self.config['OTHERS']['COPYRIGHT']

            self.pathdcp = self.config['INSTALL']['PATHDCP']
            self.pathicc = self.config['INSTALL']['PATHICC']

            self.ArgyllRes = json.loads(self.config.get('PARAMS', 'ARGYLLRES'))
            self.ArgyllAlgoritm = json.loads(self.config.get('PARAMS', 'ARGYLLALGORITM'))
            self.ArgyllUParam = json.loads(self.config.get('PARAMS', 'ARGYLLUPARAM'))
            self.Targets = json.loads(self.config.get('PARAMS', 'TARGETS'))

            self.DcamToneOperator = json.loads(self.config.get('PARAMS', 'DCAMPROFTONEOPERATOR'))
            self.DcamToneCurveDcp = json.loads(self.config.get('PARAMS', 'DCAMPROFTONECURVEDCP'))
            self.DcamIlluminant = json.loads(self.config.get('PARAMS', 'EXIFILLUMINANT'))


        else:
            print("error load configuration")

        # self.inputImage = "DSC_4453a.TIF"

        self.coodinates = []
        self.tempFolder = ""

        super(HomeUI, self).__init__(parent)
        self.ui = Ui_RoughProfiler2()
        self.ui.setupUi(self)

        # self.ui.verticalLayout.addWidget()
        self.ui.TargetType.addItems(self.Targets.keys())
        self.ui.ArgyllRes.addItems(self.ArgyllRes.keys())
        self.ui.ArgyllAlgoritm.addItems(self.ArgyllAlgoritm.keys())
        self.ui.ArgyllUparam.addItems(self.ArgyllUParam.keys())

        # self.ui.DcamprofAlgortimICC.addItems(self.DcamICCAlgoritm.keys())
        # self.ui.DcamprofTOPeratorICC.addItems(self.DcamToneOperator.keys())
        self.ui.DcamprofTOPeratoDCP.addItems(self.DcamToneOperator.keys())
        self.ui.DcamprofTOPeratoDCP.setEnabled(False)
        self.ui.DcamprofToneDCP.addItems(self.DcamToneCurveDcp.keys())
        self.ui.DcamprofToneDCP.currentTextChanged.connect(self.enableToneOperatorDCP)
        # self.ui.DcamprofToneICC.addItems(self.DcamToneCurveICC.keys())
        self.ui.DcamprofIlluminant.addItems(self.DcamIlluminant.keys())
        # self.ui.DcamprofICCResLUT.addItems(self.ICCLutResolution.keys())

        self.ui.tabWidget_2.setTabEnabled(3, False)
        self.ui.tabWidget_2.setTabEnabled(2, False)
        self.ui.tabWidget_2.setTabEnabled(1, False)
        self.ui.tabWidget_2.setTabEnabled(0, False)
        self.ui.tabWidget_2.setCurrentIndex(0)
        # --- open imagen
        self.ui.ExecuteReadImage.clicked.connect(self.readImage)
        self.ui.textEdit.setReadOnly(True)
        self.ui.OpenImage.clicked.connect(self.openTestImage)
        self.ui.OpenImage.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('picture_64px.png')))
        self.ui.OpenImage.setIconSize(QtCore.QSize(30, 30))
        # --- Load CGATS
        self.ui.LoadCGATS.setEnabled(False)
        self.ui.LoadCGATS.clicked.connect(self.openCGATS)
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
        self.ui.InstallProfile.clicked.connect(self.installProfile)
        self.ui.InstallProfile.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('saveprofile_64px.png')))
        self.ui.InstallProfile.setIconSize(QtCore.QSize(45, 45))
        # --- Create Proof image
        self.ui.createProofImage.setEnabled(False)
        self.ui.createProofImage.clicked.connect(self.createdProofimage)
        self.ui.createProofImage.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('proof_64px.png')))
        self.ui.createProofImage.setIconSize(QtCore.QSize(45, 45))

        # ---- Configuration

        self.ui.boxConfArgyll.setText(self.config['APPS']['ARGYLL'])
        self.ui.boxConfDcamprof.setText(self.config['APPS']['DCAMPROF'])
        self.ui.boxConfICCPath.setText(self.config['INSTALL']['PATHICC'])
        self.ui.boxConfDCPSystemPath.setText(self.config['INSTALL']['PATHDCP'])

        self.ui.boxConfCopyright.setText(self.config['OTHERS']['copyright'])
        self.ui.CopyRightText.setText(self.config['OTHERS']['copyright'])
        self.ui.boxConfFilenamePrefix.setText(self.config['OTHERS']['filenamesufix'])
        self.ui.boxConfDefaultModel.setText(self.config['OTHERS']['devicemodel'])


        self.ui.OpenArgyllPath.clicked.connect(lambda state, field="argyllpath": self.openConfFolder(field))
        self.ui.openDcamprofPath.clicked.connect(lambda state, field="dcamppath": self.openConfFolder(field))
        self.ui.OpenICCsystemPath.clicked.connect(lambda state, field="iccpath": self.openConfFolder(field))
        self.ui.OpenDCPsistemPath.clicked.connect(lambda state, field="dcppath": self.openConfFolder(field))

        self.ui.SaveCopyright.clicked.connect(lambda state, field="copyright": self.saveConfParams(field))
        self.ui.SaveFilenamePrefix.clicked.connect(lambda state, field="prefix": self.saveConfParams(field))
        self.ui.SaveDefaultModel.clicked.connect(lambda state, field="model": self.saveConfParams(field))


        # self.ui.tabWidget.tabBarClicked.connect(self.choiceDCPICC)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget_2.setCurrentIndex(0)


        self.ui.ARgyllUslicer.setEnabled(False)
        self.ui.ARgyllUslicer.valueChanged[int].connect(self.updateSliderLabel)
        self.ui.ArgyllEmphasisSlider.valueChanged[int].connect(self.updateSliderLabelEmphasis)
        self.ui.DcamExposureSlider.valueChanged[int].connect(self.updateSliderExposure)
        self.ui.ArgyllUparam.currentTextChanged.connect(self.enableSlider)

        self.ui.GlareCheckBox.setChecked(True)


    def updateSliderExposure(self):
        valor = self.ui.DcamExposureSlider.value()
        self.ui.exposureOffsetValue.setText(str(valor / 10))

    def updateSliderLabel(self):
        valor = self.ui.ARgyllUslicer.value()
        valor = round(valor * 0.1, 1)
        self.ui.ArgyllUscale.setText(str(valor))

    def updateSliderLabelEmphasis(self):
        valor = self.ui.ArgyllEmphasisSlider.value()
        valor = round(valor * 0.1, 1) + 1
        self.ui.ArgyllGridEmphasis.setText(str(valor))

    def enableSlider(self):
        if self.ui.ArgyllUparam.currentIndex() == 4:  # if is "custom"
            self.ui.ARgyllUslicer.setEnabled(True)

    def enableToneOperatorDCP(self):

        ToneCurveIndex = list(self.DcamToneCurveDcp)[self.ui.DcamprofToneDCP.currentIndex()]
        if ToneCurveIndex == "None" or ToneCurveIndex == "Linear":
            self.ui.DcamprofTOPeratoDCP.setEnabled(False)
        else:
            self.ui.DcamprofTOPeratoDCP.setEnabled(True)

    def enableCamToneOperator(self):
        option = list(self.DcamToneCurveICC)[self.ui.DcamprofToneICC.currentIndex()]
        if option != "none":
            self.ui.DcamprofTOPeratorICC.setEnabled(True)
        else:
            self.ui.DcamprofTOPeratorICC.setEnabled(False)

    def enableDisableICCDEP(self):

        filename = self.ui.FileNameText.text()
        if self.isRaw:
            self.ui.FileNameText.setText(filename.replace(".icc", ".dcp"))
            self.ui.Dcamprof.setEnabled(True)
            self.ui.ArgyllCM.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setCurrentIndex(1)
        else:
            self.ui.FileNameText.setText(filename.replace(".dcp", ".icc"))
            self.ui.Dcamprof.setEnabled(False)
            self.ui.ArgyllCM.setEnabled(True)
            self.ui.tabWidget.setTabEnabled(0, True)
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setCurrentIndex(0)

    # self.ui.tabsDcamprof.currentIndex()

    def DcamProfTabsOnclick(self):
        '''
        0 = DCP
        1 = ICC
        :return:
        '''
        index = self.ui.tabsDcamprof.currentIndex()

        if index == 0:
            self.ui.createProofImage.setEnabled(True)
            filename = self.ui.FileNameText.text()
            filename = filename.replace(" ", "_")
            self.ui.FileNameText.setText(filename.replace(".dcp", ".icc"))
            if self.tempFolder != "":
                self.outputICCfilename = os.path.join(self.tempFolder, self.ui.FileNameText.text())

        elif index == 1:

            self.ui.createProofImage.setEnabled(False)
            filename = self.ui.FileNameText.text()
            filename = filename.replace(" ", "_")
            self.ui.FileNameText.setText(filename.replace(".icc", ".dcp"))
            if self.tempFolder != "":
                self.outputICCfilename = os.path.join(self.tempFolder, self.ui.FileNameText.text())

    def installProfile(self):

        if os.path.isfile(self.outputICCfilename):
            icc = self.outputICCfilename
        else:
            icc = self.oldICCprofile

        print(icc)
        filename = os.path.basename(icc)
        ext = os.path.splitext(filename)[1]

        if ext == ".dcp":
            shutil.copyfile(icc, os.path.join(self.pathdcp, filename))
            if os.path.isfile(os.path.join(self.pathdcp, filename)):
                AppWarningsClass.informative_warn("Profile DCP was installed")
                print(os.path.join(self.pathdcp, filename))
                print("OK DCP")
        elif ext == ".icc":
            shutil.copyfile(icc, os.path.join(self.pathicc, filename))
            if os.path.isfile(os.path.join(self.pathicc, filename)):
                AppWarningsClass.informative_warn("Profile ICC was installed")

    def getMetadata(self, img):

        im = open(img, 'rb')
        metadata = exifread.process_file(im)
        # print(metadata)
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

        filename = self.createICCFileName(model)
        self.ui.FileNameText.setText(filename)

    def saveConfParams(self, field):
        ConfIni.saveParams(field, self.ui)

    def openConfFolder(self, field):
        startingDir = "/Users/jpereira/Python/roughprofiler2/test"
        destDir = QtGui.QFileDialog.getExistingDirectory(None,
                                                         'Open executables directory',
                                                         startingDir,
                                                         QtGui.QFileDialog.ShowDirsOnly)
        if destDir != "":
            ConfIni.openAndSavePaths(field, destDir, self.ui)


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
        # print(paths)
        if len(paths) > 0:
            self.inputImage = paths[0]
            self.ui.FileNameValue.setText(os.path.basename(paths[0]))
            self.ui.FileNameValue.repaint()

            if os.path.isfile(paths[0]):
                self.isRaw = False
                self.CEGATS_path = False
                self.ui.tabWidget_2.setTabEnabled(0, True)
                self.ui.tabWidget_2.setCurrentIndex(0)
                self.ui.ExecuteReadImage.setEnabled(True)
                self.ui.LoadCGATS.setEnabled(True)
                self.inputImage = paths[0]
                self.filename = os.path.splitext(os.path.basename(self.inputImage))[0]
                self.tempFolder = os.path.join(os.path.dirname(paths[0]), self.filename)
                self.ti3 = os.path.join(self.tempFolder, self.filename + ".ti3")
                self.diag = os.path.join(self.tempFolder, self.filename + "_diag.tiff")
                self.checkIfRawFile()
                self.getMetadata(paths[0])
                self.outputICCfilename = os.path.join(self.tempFolder, self.ui.FileNameText.text())
                self.loadImage()
                self.checkTempFolderContents()
                self.enableDisableICCDEP()

    def checkIfRawFile(self):
        '''
        if is a raw file create a thumbnail with rawpy
        :return:
        '''
        rawExt = [".DNG", ".dng", ".NEF", ".nef"]
        if os.path.splitext(os.path.basename(self.inputImage))[1] in rawExt:
            self.rawinputfile = self.inputImage
            path = os.path.join(self.tempFolder, "thumb_" + self.filename + ".tiff")

            if not os.path.isfile(path):
                self.createTempFolder()
                # rgbImage = DevelopImages.raw_get_thumbnail(self.inputImage)
                rgbImage = DevelopImages.raw_gamma_develop(self.inputImage)
                cv2.imwrite(path, rgbImage)
            if os.path.isfile(path):
                self.inputImage = path
                self.isRaw = True

        else:
            self.isRaw = False

        # self.ui.FileNameValue.repaint()  # para el bug en Mojave que no actualiza componentes

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
        index = self.ui.tabWidget.currentIndex()
        if index == 0:
            self.runColprof()
        elif index == 1:
            self.runDcamprof()

    def runDcamprof(self):
        '''
        Run Dcamprof DCP
        :return:
        '''
        output = ""
        target = list(self.Targets.values())[self.ui.TargetType.currentIndex()]
        executables = os.path.join(self.pathDcamprofExecutables, "dcamprof")
        jsonOutProfile = os.path.join(self.tempFolder, self.filename + ".json")
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        ToneCurveIndex = list(self.DcamToneCurveDcp)[self.ui.DcamprofToneDCP.currentIndex()]
        exposureOffset = self.ui.exposureOffsetValue.text()
        illuminant = self.DcamIlluminant[list(self.DcamIlluminant)[self.ui.DcamprofIlluminant.currentIndex()]]
        yLimit = self.ui.YLimitBox.text()
        filename = self.ui.FileNameText.text()

        cmd = [executables, "make-profile", "-i", illuminant, "-y", str(yLimit), self.ti3, jsonOutProfile]

        # add glare correction
        if self.ui.GlareCheckBox.isChecked():
            if target[2] != "":
                jsonInProfile = DefinePathsClass.create_reference_paths(target[2])
                cmd.insert(2, "-g")
                cmd.insert(3, jsonInProfile)
            else:
                AppWarningsClass.critical_warn("JSON target profile do not exists, please update confinguration.ini")
                self.ui.GlareCheckBox.setChecked(False)

        if self.ui.LookCorrection.isChecked():
            jsonInProfile = DefinePathsClass.create_reference_paths("lessblue.json")
            cmd.insert(2, "-a")
            cmd.insert(3, jsonInProfile)

        print(cmd)
        output, _ = self.executeTool(cmd, "Dcamprof make-profile", "dcamprof", output)

        cmd = [executables, "make-dcp", "-n", model, "-d", description, "-b", exposureOffset, jsonOutProfile,
               os.path.join(self.tempFolder, filename)]

        if ToneCurveIndex != "None":
            toneCurve = self.DcamToneCurveDcp[ToneCurveIndex]
            if ".json" in toneCurve or ".rtc" in toneCurve:
                toneCurve = DefinePathsClass.create_reference_paths(toneCurve)
            cmd.insert(2, "-t")
            cmd.insert(3, toneCurve)

            if ToneCurveIndex != "Linear":
                toneOperator = self.DcamToneOperator[
                    list(self.DcamToneOperator)[self.ui.DcamprofTOPeratoDCP.currentIndex()]]
                if ".json" in toneOperator:
                    toneOperator = DefinePathsClass.create_reference_paths(toneOperator)
                cmd.insert(4, "-o")
                cmd.insert(5, toneOperator)

        print(cmd)
        if os.path.isfile(jsonOutProfile):
            self.executeTool(cmd, "Dcamprof make-dcp", "dcamprof", output)

        if os.path.isfile(self.outputICCfilename):
            self.oldICCprofile = self.outputICCfilename
            self.createICCFileName(rootname="")
            self.ui.InstallProfile.setEnabled(True)

    '''def runDcamprofICC(self):
        #dcamprof make-profile -g cc24-layout.json new-target.ti3 profile.json
        #dcamprof make-icc -n "Camera manufacturer and model" -f target.tif -t acr profile.json profile.icc
        output = ""
        target = list(self.Targets.values())[self.ui.TargetType.currentIndex()]
        executables = os.path.join(self.pathDcamprofExecutables, "dcamprof")
        jsonOutProfile = os.path.join( self.tempFolder, self.filename+".json" )
        #iccFile = os.path.join( self.tempFolder, self.filename+".icc" )
        copyright = self.ui.CopyRightText.text()
        model = self.ui.ModelText.text()
        toneCurve = self.DcamToneCurveICC[ list(self.DcamToneCurveICC)[self.ui.DcamprofToneICC.currentIndex()]]
        toneOperator = self.DcamToneOperator[ list(self.DcamToneOperator)[self.ui.DcamprofTOPeratorICC.currentIndex()]]
        algoritm = self.DcamICCAlgoritm[ list(self.DcamICCAlgoritm)[self.ui.DcamprofAlgortimICC.currentIndex()] ]
        illuminant = self.DcamIlluminant[ list(self.DcamIlluminant)[self.ui.DcamprofIlluminant.currentIndex()] ]
        lutRes = self.ICCLutResolution[ list(self.ICCLutResolution)[self.ui.DcamprofICCResLUT.currentIndex()] ]
        yLimit = self.ui.YLimitBox.text()
        filename = self.ui.FileNameText.text()

        #dcamreports = os.path.join(self.tempFolder, "dcamreports")

        #if not os.path.isdir(dcamreports):
            #os.mkdir(dcamreports)

        print(toneCurve)
        if "curve" in toneCurve:
            toneCurve = DefinePathsClass.create_reference_paths(toneCurve)

        print(toneOperator)
        if "json" in toneOperator:
            toneOperator = DefinePathsClass.create_reference_paths(toneOperator)


        #cmd = [executables, "tiff-tf", ]

        cmd = [executables, "make-profile", "-n", model, "-i", illuminant,"-y", str(yLimit), self.ti3,  jsonOutProfile  ]

        if self.ui.GlareCheckBox.isChecked():
            jsonInProfile = DefinePathsClass.create_reference_paths(target[2])
            cmd.insert(8, "-g")
            cmd.insert(9, jsonInProfile)

        if self.ui.LookCorrection.isChecked():
            #look = "/Users/jpereira/Python/roughprofiler2/reference/ntro_conf.json"
            #cmd.insert(6, "-a")
            #cmd.insert(7, look)
            look = "/Users/jpereira/Python/roughprofiler2/test/co/lineal_curve.json"
            cmd.insert(8, "-f")
            cmd.insert(9, self.inputImage)

        print(cmd)
        output, _ = self.executeTool(cmd, "Dcamprof make-profile", "dcamprof", output )

        #with open(os.path.join(self.tempFolder, "log.txt"), 'a') as f:
            #f.write(output)

        if os.path.isfile(jsonOutProfile):
            cmd = [executables, "make-icc", "-n", model,"-s", str(lutRes), "-c", copyright, "-p", algoritm,"-t", toneCurve,"-o", toneOperator, jsonOutProfile, os.path.join(self.tempFolder, filename) ]
            print(cmd)
            output, _ = self.executeTool(cmd, "Dcamprof make-icc", "dcamprof", output)

            if os.path.isfile(self.outputICCfilename):
                self.runProfCheck(output)
                self.oldICCprofile = self.outputICCfilename
                self.ui.createProofImage.setEnabled(True)
                self.ui.InstallProfile.setEnabled(True)
                filename = self.createICCFileName(os.path.basename(self.outputICCfilename))
                self.outputICCfilename = os.path.join(self.tempFolder, filename.replace(" ", "_") + ".icc")
                self.ui.FileNameText.setText(filename.replace(" ", "_") + ".icc")
                self.ui.DestText.setText(filename.replace("_", " "))'''

    def runProfCheck(self, output):

        executable = os.path.join(self.pathArgyllExecutables, "profcheck")

        cmd = [executable, "-v2", "-Ir", self.ti3, self.outputICCfilename]

        _, proofdata = self.executeTool(cmd, "PROFCHECK", "argyll", output)

        self.loadProofChart(proofdata)
        self.loadProofDELChart(proofdata)
        self.loadProofDECChart(proofdata)
        self.loadProofDEHChart(proofdata)
        # a = ColorProof()
        # a.createJson(proofdata)

    def runColprof(self):
        '''
        run ArgyllCMS Colprof
        :return:
        '''

        manufacturer = self.ui.ManufacturerText.text()
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        copyright = self.ui.CopyRightText.text()
        argyllAlgoritm = self.ArgyllAlgoritm[list(self.ArgyllAlgoritm)[self.ui.ArgyllAlgoritm.currentIndex()]]
        argyllRes = self.ArgyllRes[list(self.ArgyllRes)[self.ui.ArgyllRes.currentIndex()]]
        argyllUParam = self.ArgyllUParam[list(self.ArgyllUParam)[self.ui.ArgyllUparam.currentIndex()]]

        if self.ui.ArgyllUparam.currentIndex() == 4:  # if is "custom"
            valor = self.ui.ARgyllUslicer.value()
            argyllUParam = "-U" + str(round(valor * 0.1, 1) * 1)

        emphasis = self.ui.ArgyllEmphasisSlider.value()
        emphasis = "-V" + str(round(emphasis * 0.1, 1) + 1)

        executable = os.path.join(self.pathArgyllExecutables, "colprof")

        cmd = [executable, "-v", "-a", argyllAlgoritm, "-bn", "-q", argyllRes, emphasis, argyllUParam, "-O",
               self.outputICCfilename, "-A", manufacturer, "-M", model, "-D", description, "-C", copyright,
               os.path.splitext(self.ti3)[0]]
        print(cmd)
        output, _ = self.executeTool(cmd, "COLPROF", "argyll", output="")

        if os.path.isfile(self.outputICCfilename):
            self.runProfCheck(output)
            self.oldICCprofile = self.outputICCfilename
            self.ui.createProofImage.setEnabled(True)
            self.ui.InstallProfile.setEnabled(True)
            self.createICCFileName(rootname="")

    def createdProofimage(self):

        if os.path.isfile(self.outputICCfilename):
            icc = self.outputICCfilename
        else:
            icc = self.oldICCprofile

        CreateProofImage(self.inputImage, icc, self.ui, self.tempFolder)

        name_orig, ext_orig = os.path.splitext(os.path.basename(icc))
        file = os.path.join(self.tempFolder, name_orig + ".tiff")

        if os.path.isfile(file):
            AppWarningsClass.informative_warn("Image " + name_orig + ".tiff" + " was create ")

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
            elif i[1] < 1:
                return False
            elif i[0] < 1:
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

        if len(self.coodinates) > 0:
            if self.checkCoordinatesInside():
                target = list(self.Targets.values())[self.ui.TargetType.currentIndex()]
                # scanin -v -p -dipn rawfile.tif ColorChecker.cht cc24_ref.cie
                executable = os.path.join(self.pathArgyllExecutables, "scanin")
                # recogfile = os.path.join( self.pathRepo, target[1])
                # reference = os.path.join(self.pathRepo, target[0])
                if not self.CEGATS_path:
                    reference = DefinePathsClass.create_reference_paths(target[0])
                else:
                    reference = self.CEGATS_path

                recogfile = DefinePathsClass.create_reference_paths(target[1])

                if not os.path.isfile(recogfile):
                    print("error no se encuenta")
                else:

                    # coordinate to string
                    res = []
                    for i in self.coodinates:
                        for j in i:
                            res.append(str(round(j, 2)))
                    coor = ",".join(res)

                    cmd = [executable, "-v2", "-p", "-dipn", self.gamma, "-F", coor, "-O", self.ti3, self.inputImage,
                           recogfile, reference, self.diag]
                    print(" ".join(cmd))
                    self.executeTool(cmd, "SCANIN", "argyll", output="")

                    if os.path.isfile(self.ti3):
                        # enable ICC/DCP buton
                        self.ui.ExecuteTask.setEnabled(True)
                    if os.path.isfile(self.diag):
                        # load diag image
                        self.loadDiag()
                        self.ui.tabWidget_2.setTabEnabled(1, True)
                        self.ui.tabWidget_2.setCurrentIndex(1)
            else:
                return AppWarningsClass.critical_warn("There are coordinates outside!")
        else:
            return AppWarningsClass.critical_warn("Select a region of interest first")

    def executeTool(self, cmd, toolName, workflow, output):
        '''
        Execute binary files
        :param cmd: list of params
        :param toolName: string with name of tool for informative log
        :return:
        '''

        self.ui.textEdit.clear()
        proofcheckOutput = []

        if output != "":
            # print(output)
            self.ui.textEdit.insertPlainText(output)

        self.ui.tabWidget_2.setCurrentIndex(2)
        self.ui.tabWidget_2.setTabEnabled(2, True)

        self.ui.textEdit.insertPlainText("---- " + toolName + "-----\n")
        QApplication.processEvents()

        cmd = list(filter(None, cmd))
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, bufsize=1)

        if workflow == "dcamprof":
            output = p.stderr.readline
        elif workflow == "argyll":
            output = p.stdout.readline

        proof = ColorProof()
        for line in iter(output, b''):
            if toolName == "PROFCHECK":
                item = proof.formatProfCheck(line.decode('utf-8'))
                proofcheckOutput.append(item)
                self.ui.textEdit.insertPlainText(proof.itemTostring(item))
            else:
                txt = line.decode('utf-8')
                self.ui.textEdit.insertPlainText(txt)

            self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
            QApplication.processEvents()

        p.stdout.close()
        p.wait()
        # print(proofcheckOutput)
        return self.ui.textEdit.toPlainText(), proofcheckOutput

    def convertLabtoHex(self, L, a, b):
        lab = LabColor(L, a, b)
        RGB = convert_color(lab, sRGBColor)
        hex = RGB.get_rgb_hex()
        return hex

    def loadDiag(self):
        '''
        Load the diag tiff files result from ArgyllCMS scanin
        :return:
        '''

        if os.path.isfile(self.diag):
            image_data = cv2.imread(self.diag)
            if image_data is not None:
                # clean widgets before
                for i in reversed(range(self.ui.verticalLayout_2.count())):
                    self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)

                graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
                graphicsView.setObjectName("graphicsView")
                v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
                v2a.setMouseEnabled(x=False, y=False)
                v2a.setLimits(xMin=0, xMax=self.lay_w)
                v2a.setAspectLocked()
                v2a.disableAutoRange('xy')

                image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
                image_data = image_data.astype(np.uint16)

                image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)
                # image apear flip in viewBox ¿?
                image_data = cv2.flip(image_data, 0)
                imageitem = pg.ImageItem(image_data, axisOrder='row-major')
                v2a.addItem(imageitem)
                v2a.autoRange()

                self.ui.verticalLayout_2.addWidget(graphicsView)
            else:
                AppWarningsClass.informative_warn("Diag file is corrupt")


    def loadProofChart(self, data):

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab.count())):
                self.ui.verticalLayout_prooftab.itemAt(i).widget().setParent(None)

            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot1')

            xlab = []
            ticks = []
            colors = []
            i = 0
            data.pop(0)
            data.pop()
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                xlab.append(float(item[1]))
                colors.append(item[2])
                ticks.append((i, item[0]))
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)

            self.ui.verticalLayout_prooftab.addWidget(window)
            self.ui.tabWidget_2.setTabEnabled(3, True)
            self.ui.tabWidget_2.setCurrentIndex(3)
        else:
            self.ui.tabWidget_2.setTabEnabled(3, False)

    def loadProofDELChart(self, data):

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEL.count())):
                self.ui.verticalLayout_prooftab_DEL.itemAt(i).widget().setParent(None)

            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot1')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                xlab.append(float(item[3][0]))
                colors.append(item[2])
                ticks.append((i, item[0]))
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEL.addWidget(window)

    def loadProofDECChart(self, data):

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEC.count())):
                self.ui.verticalLayout_prooftab_DEC.itemAt(i).widget().setParent(None)

            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot1')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                ticks.append((i, item[0]))
                xlab.append(float(item[3][1]))
                colors.append(item[2])
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEC.addWidget(window)

    def loadProofDEHChart(self, data):

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEH.count())):
                self.ui.verticalLayout_prooftab_DEH.itemAt(i).widget().setParent(None)

            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(self.lay_w, self.lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot1')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                ticks.append((i, item[0]))
                xlab.append(float(item[3][2]))
                colors.append(item[2])
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEH.addWidget(window)

    def loadImage(self):
        '''
        Load proof image on main layout, first tab
        :return:
        '''

        # clean widgets before
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

        image_data = cv2.imread(self.inputImage)
        if image_data is not None:
            self.gammaImageSize = image_data.shape
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
            image_data = image_data.astype(np.uint16)
            image_data, self.factor = self.image_resize(image_data, width=self.lay_w, height=None, inter=cv2.INTER_AREA)

            imageitem = pg.ImageItem(image_data, axisOrder='row-major')

            v2a.addItem(imageitem)
            v2a.addItem(self.createROI())  # load ROI
            v2a.autoRange()

            self.ui.verticalLayout.addWidget(graphicsView)

        else:
            AppWarningsClass.informative_warn("Image file is corrupt")

    def createROI(self):
        '''
        Create Region Of Interest
        :return:
        '''

        centro = [self.lay_w / 2, self.lay_h / 2]
        ratio = self.lay_w / self.lay_h
        top_left = [centro[0] - self.pad_roi * ratio / 2, centro[1] - self.pad_roi / 2]

        my_roi = pg.ROI(top_left, [self.pad_roi * ratio, self.pad_roi], pen=pg.mkPen(width=4.5, color='r'))

        my_roi.addScaleHandle([1, 1], [0, 0], lockAspect=False)
        my_roi.addScaleHandle([0, 0], [1, 1], lockAspect=False)
        my_roi.addScaleHandle([1, 0], [0, 1], lockAspect=False)
        my_roi.addScaleHandle([0, 1], [1, 0], lockAspect=False)
        my_roi.addRotateHandle([1, 0.5], [0.5, 0.5])
        my_roi.sigRegionChangeFinished.connect(lambda roi: self.createCoordinates(roi))

        return my_roi

    def rotate_via_numpy(self, xy, degrees):
        '''
        Rotate ROI after scale
        :param xy:
        :param degrees:
        :return:
        '''
        # https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302

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
        # corrige la rotación sino la hace al contrario ¿?
        angle = state['angle'] * -1

        top_left = self.rotate_via_numpy((x, y), angle)
        top_right = self.rotate_via_numpy((w + x, y), angle)
        bottom_right = self.rotate_via_numpy((w + x, h + y), angle)
        bottom_left = self.rotate_via_numpy((x, h + y), angle)

        self.coodinates = [top_left, top_right, bottom_right, bottom_left]
        # print(self.coodinates)

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
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

        resized = cv2.resize(image, dim, interpolation=inter)

        (h1, w1) = resized.shape[:2]
        factor = w / w1

        return resized, factor

    def createICCFileName(self, rootname):

        if self.isRaw:
            ext = "dcp"
        else:
            ext = "icc"

        if rootname != "":
            rootname = rootname + "_"

        num = 0
        if os.path.isdir(self.tempFolder):
            files = glob.glob(os.path.join(self.tempFolder, "*." + ext))
            files.sort(key=os.path.getmtime)
            if len(files) > 0:
                last = files[-1]
                last = os.path.basename(last)
                name_orig, ext_orig = os.path.splitext(last)
                serie = name_orig[-3:]
                num = int(serie) + 1
                rootname = name_orig[:-3]

        counter = f"{num:0>3}"
        filename = "{0}{1}.{2}".format(rootname, counter, ext)
        filename = filename.replace(" ", "_")
        self.ui.FileNameText.setText(filename)
        self.outputICCfilename = os.path.join(self.tempFolder, filename)
        self.ui.DestText.setText(rootname.replace("_", " ") + " " + str(counter))

        return filename


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = HomeUI()
    main.show()
    sys.exit(app.exec_())

