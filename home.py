
import pyqtgraph as pg
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QEvent
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
from presets import PresetManagement
import webbrowser
import  getpass

class HomeUI(QtWidgets.QDialog):

    def __init__(self, parent=None):


        super(HomeUI, self).__init__(parent)
        self.ui = Ui_RoughProfiler2()
        self.ui.setupUi(self)

        self.pathArgyllExecutables = ""
        self.pathDcamprofExecutables = ""

        self.loadConfigurationINI()

        self.coodinates = []
        self.tempFolder = ""
        self.inputImage = ""
        self.CEGATS_path = r""


        #if folder with programs exists, populate it

        #check if Argyll or Dcamprof exists
        if self.pathArgyllExecutables == "" or self.pathDcamprofExecutables == "":
            if not ConfIni.programsAutoPath(self.ui):
                AppWarningsClass.informative_warn("ArgyllCMS paths or DCAMPROF paths are missing in configuration file, please define before start")
                self.ui.tabWidget_2.setCurrentIndex(3)
                self.ui.OpenImage.setEnabled(False)
            else:
                self.loadConfigurationINI()
        elif not os.path.isdir(self.pathArgyllExecutables):
            AppWarningsClass.informative_warn("ArgyllCMS paths was defined but currently is missing")
            self.ui.tabWidget_2.setCurrentIndex(3)
            self.ui.OpenImage.setEnabled(False)
        elif not os.path.isdir(self.pathDcamprofExecutables):
            AppWarningsClass.informative_warn("Dcamprof paths was defined but currently is missing")
            self.ui.tabWidget_2.setCurrentIndex(3)
            self.ui.OpenImage.setEnabled(False)
        else:
            self.ui.OpenImage.setEnabled(True)


        #---- main tabs
        self.ui.tabWidget_2.setTabEnabled(3, False)
        self.ui.tabWidget_2.setTabEnabled(2, False)
        self.ui.tabWidget_2.setTabEnabled(1, False)
        self.ui.tabWidget_2.setTabEnabled(0, False)
        #self.ui.tabWidget_2.setCurrentIndex(0)
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
        # --- Argyll Dcamproof URLS
        self.ui.ArgyllOpenSite.clicked.connect(self.openArgyllCMSSite)
        self.ui.DCamprofOpenSite.clicked.connect(self.openDcamprofSite)

        #---- open pach tuning file
        self.ui.OpenTuningFile.clicked.connect(self.openTuningFile)


        # ---- Configuration

        if self.config['INSTALL']['PATHICC'] == "" and self.config['INSTALL']['PATHDCP'] == "":
            ConfIni.getuserpaths(self.ui)
        else:
            self.ui.boxConfICCPath.setText(self.config['INSTALL']['PATHICC'])
            self.ui.boxConfDCPSystemPath.setText(self.config['INSTALL']['PATHDCP'])

        self.ui.OpenArgyllPath.clicked.connect(lambda state, field="argyllpath": self.openConfFolder(field))
        self.ui.openDcamprofPath.clicked.connect(lambda state, field="dcamppath": self.openConfFolder(field))
        self.ui.OpenICCsystemPath.clicked.connect(lambda state, field="iccpath": self.openConfFolder(field))
        self.ui.OpenDCPsistemPath.clicked.connect(lambda state, field="dcppath": self.openConfFolder(field))

        self.ui.SaveCopyright.clicked.connect(lambda state, field="copyright": self.saveConfParams(field))
        self.ui.SaveFilenamePrefix.clicked.connect(lambda state, field="prefix": self.saveConfParams(field))
        self.ui.SaveDefaultModel.clicked.connect(lambda state, field="model": self.saveConfParams(field))

        # --------- History Combo
        self.ui.HistoryCombo.setEnabled(False)
        self.ui.HistoryCombo.currentTextChanged.connect(self.loadhistorypreset)

        self.ui.tabWidget.setCurrentIndex(0)

        self.ui.ARgyllUslicer.setEnabled(False)
        self.ui.ARgyllUslicer.valueChanged[int].connect(self.updateSliderLabel)
        self.ui.ArgyllEmphasisSlider.valueChanged[int].connect(self.updateSliderLabelEmphasis)
        self.ui.DcamExposureSlider.valueChanged[int].connect(self.updateSliderExposure)
        self.ui.ArgyllUparam.currentTextChanged.connect(self.enableSlider)

        self.printInfo("Hello! This is a free app from Jose Pereira, www.jpereira.net")

        #self.printInfo( getpass.getuser() +" "+ os.getlogin()+" "+os.path.expanduser('~') )



    def loadConfigurationINI(self):
        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")

        if os.path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.pathArgyllExecutables = self.config['APPS']['ARGYLL']
            self.pathDcamprofExecutables = self.config['APPS']['DCAMPROF']
            self.ui.boxConfArgyll.setText(self.config['APPS']['ARGYLL'])
            self.ui.boxConfDcamprof.setText(self.config['APPS']['DCAMPROF'])
            self.pathdcp = self.config['INSTALL']['PATHDCP']
            self.pathicc = self.config['INSTALL']['PATHICC']

            self.pad_roi = int(self.config['LAYOUT']['PAD_ROI'])

            self.ArgyllRes = json.loads(self.config.get('PARAMS', 'ARGYLLRES'))
            self.ui.ArgyllRes.addItems(self.ArgyllRes.keys())
            self.ArgyllAlgoritm = json.loads(self.config.get('PARAMS', 'ARGYLLALGORITM'))
            self.ui.ArgyllAlgoritm.addItems(self.ArgyllAlgoritm.keys())

            self.ArgyllUParam = json.loads(self.config.get('PARAMS', 'ARGYLLUPARAM'))
            self.ui.ArgyllUparam.addItems(self.ArgyllUParam.keys())

            self.Targets = json.loads(self.config.get('PARAMS', 'TARGETS'))
            self.ui.TargetType.addItems(self.Targets.keys())
            self.ui.TargetType.currentTextChanged.connect(self.checkReferences)

            self.DcamToneOperator = json.loads(self.config.get('PARAMS', 'DCAMPROFTONEOPERATOR'))
            self.ui.DcamprofTOPeratoDCP.addItems(self.DcamToneOperator.keys())
            self.ui.DcamprofTOPeratoDCP.setEnabled(False)

            self.DcamToneCurveDcp = json.loads(self.config.get('PARAMS', 'DCAMPROFTONECURVEDCP'))
            self.ui.DcamprofToneDCP.addItems(self.DcamToneCurveDcp.keys())
            self.ui.DcamprofToneDCP.currentTextChanged.connect(self.enableToneOperatorDCP)

            self.DcamIlluminant = json.loads(self.config.get('PARAMS', 'EXIFILLUMINANT'))
            self.ui.DcamprofIlluminant.addItems(self.DcamIlluminant.keys())

            self.ui.boxConfCopyright.setText(self.config['OTHERS']['copyright'])
            self.ui.CopyRightText.setText(self.config['OTHERS']['copyright'])
            self.ui.CopyRightText.repaint()

            self.ui.boxConfFilenamePrefix.setText(self.config['OTHERS']['filenamesufix'])
            self.ui.boxConfDefaultModel.setText(self.config['OTHERS']['devicemodel'])

        else:
            AppWarningsClass.critical_warn("Configuration cannot loaded check confinguration.ini file on configuration folder")

    def event(self, event):
        if event.type() == QEvent.EnterWhatsThisMode:
            AppWarningsClass.informative_warn("RoughProfiler is a free GUI software for ArgyllCMS by Graeme W. Gill (https://www.argyllcms.com/)"
                                              " and DCamProf by Anders Torger (https://torger.se/anders/dcamprof.html)"
                                              "developed by Jose Pereira (info@jpereira.net)")
            return True
        return QDialog.event(self, event)

    def openArgyllCMSSite(self):
        url = "https://www.argyllcms.com/"
        webbrowser.open(url, new=0, autoraise=True)

    def openDcamprofSite(self):
        url = "https://torger.se/anders/dcamprof.html#download"
        webbrowser.open(url, new=0, autoraise=True)


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
        else:
            self.ui.ARgyllUslicer.setEnabled(False)
            self.ui.ArgyllUscale.setText("1.0")
            self.ui.ARgyllUslicer.setValue(1)

    def printInfo(self, msg):
        self.ui.infoBox.setText(msg)
        self.ui.infoBox.repaint()

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

    def defineExtensions(self, exts):
        '''
        Create extension from configuration
        :param exts:
        :return:
        '''
        extensions = exts.split(sep=",")
        s = []
        r = []
        for ext in extensions:
            s.append("*."+ext.replace(" ", ""))
            s.append("*." + ext.replace(" ", "").upper() )
            r.append(ext.replace(" ", ""))
            r.append(ext.replace(" ", "").upper())

        cadena = " ".join(s)
        return cadena, r

    def checkReferences(self):
        if self.inputImage:
            self.CEGATS_path = r""
            self.ui.ReferenceNameValue.setText("")
            self.ui.ReferenceNameValue.repaint()
            self.reference = ""
            self.checkTargets()

    def resetReferences(self):

        if self.inputImage:
            self.ui.ExecuteReadImage.setEnabled(False)
            self.ui.ExecuteReadImage.repaint()
            self.ui.TargetType.setCurrentIndex(0)
            self.CEGATS_path = r""
            self.ui.ReferenceNameValue.setText("")
            self.ui.ReferenceNameValue.repaint()
            self.reference = ""
            self.checkTargets()

    def checkTargets(self):
        '''
        Check if Reference, recognition an json dcamprof profiles exists
        :return:
        '''

        targetComoboIndex = self.ui.TargetType.currentIndex()
        if targetComoboIndex > 0:
            target = list(self.Targets.values())[targetComoboIndex]
            cgats = DefinePathsClass.create_reference_paths(target[0])
            recog = DefinePathsClass.create_reference_paths(target[1])
            profile = DefinePathsClass.create_reference_paths(target[2])

            #check if CGATS exists
            if not os.path.isfile(cgats) and not os.path.isfile(self.CEGATS_path):
                self.printInfo("CGATS reference file do not exits! You must load it")
                AppWarningsClass.informative_warn("CGATS reference file do not exits! you must load it")
            else:
                if os.path.isfile(self.CEGATS_path):
                    self.reference = self.CEGATS_path
                elif os.path.isfile(cgats):
                    self.reference = cgats

                self.ui.ReferenceNameValue.setText(os.path.basename(os.path.basename(self.reference)))
                self.ui.ReferenceNameValue.repaint()
                #self.ui.ExecuteReadImage.setEnabled(True)

            #check if recognition file exists
            if not os.path.isfile(recog):
                    self.printInfo("Recognition file ("+target[1]+") lost!")
                    AppWarningsClass.informative_warn("Recognition file lost! Check reference folder o configuration.ini")
            else:
                self.recogfile = recog

            #check referece and recognition
            if os.path.isfile(self.recogfile) and os.path.isfile(self.reference) and os.path.isfile(self.inputImage):
                self.ui.ExecuteReadImage.setEnabled(True)
                self.ui.ReferenceNameValue.repaint()
            else:
                self.ui.ExecuteReadImage.setEnabled(False)
                self.ui.ExecuteReadImage.repaint()


            #check if Dcamprof json profile exists
            if not os.path.isfile(profile):
                #self.printInfo("JSON Dcamproof profile do not exits!")
                self.ui.GlareCheckBox.setEnabled(False)
                self.jsonDcamProfile = False
            else:
                self.jsonDcamProfile = profile
                self.ui.GlareCheckBox.setEnabled(True)

    def loadhistorypreset(self):
        '''
        When a preset (history) is set, his values are load
        :return:
        '''
        index = self.ui.HistoryCombo.currentIndex()
        #mode =  self.ui.tabWidget.currentIndex()
        if index > 0:
            self.printInfo("Loading old settings")
            preset = self.presets[index]
            jsonFile = os.path.join(self.tempFolder, preset+".json" )
            self.oldICCprofile =  os.path.join(self.tempFolder, preset+".icc" )

            data = PresetManagement.setParams(self.ui,jsonFile)
            if data["proofdata"]:
                self.loadProofChart(data["proofdata"])
                self.loadProofDELChart(data["proofdata"])
                self.loadProofDECChart(data["proofdata"])
                self.loadProofDEHChart(data["proofdata"])
                self.ui.tabWidget_2.setCurrentIndex(3)

            if not self.isRaw:
                self.ui.createProofImage.setEnabled(True)

            self.ui.InstallProfile.setEnabled(True)

    def updateHistoryCombo(self):
        '''
        Populate the combobox history with the old history presets
        :return:
        '''
        self.presets = PresetManagement.populateHistoryCombo(self.tempFolder)
        if len(self.presets) > 1:
            self.ui.HistoryCombo.clear()
            self.ui.HistoryCombo.addItems(self.presets)
            self.ui.HistoryCombo.setEnabled(True)
            self.ui.HistoryCombo.repaint()
        else:
            self.ui.HistoryCombo.clear()
            self.ui.HistoryCombo.setEnabled(False)
            self.ui.HistoryCombo.repaint()


    def enableDisableICCDEP(self):
        '''
        if is a raw file or not, enable or disable differents butons and options
        :return:
        '''
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


    def installProfile(self):
        '''
        Copy profile to system path
        :return:
        '''
        if os.path.isfile(self.outputICCfilename):
            icc = self.outputICCfilename
        else:
            #print(self.oldICCprofile)
            icc = self.oldICCprofile

        #print(icc)
        filename = os.path.basename(icc)
        ext = os.path.splitext(filename)[1]

        if ext == ".dcp":
            if os.path.isdir(self.pathdcp):
                shutil.copyfile(icc, os.path.join(self.pathdcp, filename))
                if os.path.isfile(os.path.join(self.pathdcp, filename)):
                    AppWarningsClass.informative_warn("Profile DCP was installed")
                    self.printInfo("Profile "+filename+" was installed")
                    #print(os.path.join(self.pathdcp, filename))
            else:
                self.printInfo("Camera profiles folder not found")
        elif ext == ".icc":
            if os.path.isdir(self.pathicc):
                shutil.copyfile(icc, os.path.join(self.pathicc, filename))
                if os.path.isfile(os.path.join(self.pathicc, filename)):
                    AppWarningsClass.informative_warn("Profile ICC was installed")
                    self.printInfo("Profile " + filename + " was installed")
                else:
                    self.printInfo("ICC folder not found")

    def getMetadata(self, img):
        '''
        Read metadata from image for model info
        :param img:
        :return:
        '''

        im = open(img, 'rb')
        metadata = exifread.process_file(im)

        if 'Image Make' in metadata and str(metadata['Image Make']) != "":
            manufacturer = str(metadata['Image Make'])
        else:
            manufacturer = "Manufacturer"

        if 'Image Model' in metadata and str(metadata['Image Model']) != "":
            model = str(metadata['Image Model'])
        else:
            model = self.config["OTHERS"]["devicemodel"]
            if model == "":
                model = "no-model"


        self.ui.ManufacturerText.setText(manufacturer)
        self.ui.ModelText.setText(model)

        filename = self.createICCFileName(model)
        self.ui.FileNameText.setText(filename)

    def saveConfParams(self, field):
        ConfIni.saveParams(field, self.ui)

    def openConfFolder(self, field):
        std = False
        startingDir = self.config['PATHS']['lastfolder']
        destDir = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                         'Open executables directory',
                                                         startingDir,
                                                         QtWidgets.QFileDialog.ShowDirsOnly)
        if destDir != "":
            std = ConfIni.openAndSavePaths(field, destDir, self.ui)

        if std:
            self.loadConfigurationINI()

    def openTuningFile(self):
        '''
        Open a JSON file with tuning info
        https://torger.se/anders/dcamprof.html#make_profile_deep_blue
        :return:
        '''
        path = self.config['PATHS']['lastfolder']
        qfd = QtWidgets.QFileDialog()
        filter = "JSON Files (*.json)"
        title = "Open JSON Tuning file"
        fname = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
        if fname != "":
            self.ui.boxTuningFilePath.setText(fname)
            self.dcamproftuningfile = fname
        else:
            self.ui.boxTuningFilePath.setText("")

        self.printInfo("When tuning file is loading, process can become very slow")


    def checkIfASCII(self,cadena):
        if not cadena.isascii():
            AppWarningsClass.informative_warn("Image path has non ASCII characters some functions may not run. Please remove this characters from path and open again ")


    def openTestImage(self):
        '''
        Open test image dialog
        :return:
        '''

        path = self.config['PATHS']['lastfolder']
        qfd = QtWidgets.QFileDialog()
        extensions, _ = self.defineExtensions( self.config['OTHERS']['fileext']+', '+self.config['OTHERS']['rawfileext'] )
        paths = [str(file_n) for file_n in list(
            QtWidgets.QFileDialog.getOpenFileNames(qfd, "Select files", path,
                                                   filter='Images ('+extensions+')'
                                                   )[0])]
        # print(paths)
        if len(paths) > 0:
            self.checkIfASCII(paths[0])
            self.inputImage = paths[0]
            self.ui.FileNameValue.setText(os.path.basename(paths[0]))
            self.ui.FileNameValue.repaint()
            ConfIni.savelastpath(os.path.dirname(paths[0]))

            if os.path.isfile(paths[0]):
                self.isRaw = False
                #self.CEGATS_path = r""
                self.ui.tabWidget_2.setTabEnabled(0, True)
                self.ui.tabWidget_2.setCurrentIndex(0)
                self.ui.LoadCGATS.setEnabled(True)
                self.inputImage = paths[0]
                self.filename = os.path.splitext(os.path.basename(self.inputImage))[0]
                self.tempFolder = os.path.join(os.path.dirname(paths[0]), self.filename)
                self.ti3 = os.path.join(self.tempFolder, self.filename + ".ti3")
                self.diag = os.path.join(self.tempFolder, self.filename + "_diag.tiff")
                self.outputICCfilename = os.path.join(self.tempFolder, self.ui.FileNameText.text())
                self.resetReferences()
                self.checkIfRawFile()
                self.getMetadata(paths[0])
                self.loadImage()
                self.checkTempFolderContents()
                self.enableDisableICCDEP()
                self.clearDeltas()
                self.updateHistoryCombo()

                #PresetManagement.readLastPreset(self.ui, self.tempFolder)



    def checkIfRawFile(self):
        '''
        if is a raw file create a thumbnail with rawpy
        :return:
        '''
        #self.config['OTHERS']['rawfileext']
        _, rawExt  = self.defineExtensions( self.config['OTHERS']['rawfileext'] )
        if os.path.splitext(os.path.basename(self.inputImage))[1].replace(".","") in rawExt:

            self.printInfo("File is in raw format, running develop process, wait...")
            self.rawinputfile = self.inputImage
            path = os.path.join(self.tempFolder, "thumb_" + self.filename + ".tiff")

            if not os.path.isfile(path):

                self.createTempFolder()
                # rgbImage = DevelopImages.raw_get_thumbnail(self.inputImage)
                rgbImage = DevelopImages.raw_gamma_develop(self.inputImage)
                #cv2.imwrite(path, rgbImage)  #fail with special "latin" chars on path
                #to save in a path with special chars
                is_success, im_buf_arr = cv2.imencode(".tiff", rgbImage)
                im_buf_arr.tofile(path)

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
        path = self.config['PATHS']['lastfolder']

        filter = "Images (*.txt *.cie)"
        title = "GET CGATS"
        fname = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filter)[0]

        #print(type(fname))

        if os.path.isfile(fname):
            self.CEGATS_path = fname
            self.ui.ReferenceNameValue.setText(os.path.basename(self.CEGATS_path))
            self.printInfo("Loading CGATS file")
            self.checkTargets()

    def executeProcess(self):
        '''
        Execute ArgyllCMS o Dcamprof workflows
        :return:
        '''
        index = self.ui.tabWidget.currentIndex()
        if index == 0:
            self.printInfo("Calling for Colprof")
            self.runColprof()
        elif index == 1:
            self.printInfo("Calling for Decamprof")
            self.runDcamprof()

    def runDcamprof(self):
        '''
        Run Dcamprof DCP
        :return:
        '''
        output = ""
        #target = list(self.Targets.values())[self.ui.TargetType.currentIndex()]
        executables = os.path.join(self.pathDcamprofExecutables, "dcamprof")
        jsonOutProfile = os.path.join(self.tempFolder, self.filename + ".json")
        model = self.ui.ModelText.text()
        description = self.ui.DestText.text()
        ToneCurveIndex = list(self.DcamToneCurveDcp)[self.ui.DcamprofToneDCP.currentIndex()]
        exposureOffset = self.ui.exposureOffsetValue.text()
        illuminant = self.DcamIlluminant[list(self.DcamIlluminant)[self.ui.DcamprofIlluminant.currentIndex()]]
        yLimit = self.ui.YLimitBox.text()
        filename = self.ui.FileNameText.text()

        self.ti3 = self.ti3.encode('utf-8','ignore').decode("utf-8")
        jsonOutProfile = jsonOutProfile.encode('utf-8','ignore').decode("utf-8")
        filename = filename.encode('utf-8','ignore').decode("utf-8")

        # this is a non-ascii character. Do something.

        cmd = [executables, "make-profile", "-i", illuminant, "-y", str(yLimit), self.ti3, jsonOutProfile]

        # add glare correction
        if self.ui.GlareCheckBox.isChecked():
            if self.jsonDcamProfile:
                cmd.insert(2, "-g")
                cmd.insert(3, self.jsonDcamProfile )
            else:
                AppWarningsClass.critical_warn("JSON target profile do not exists, please update confinguration.ini")
                self.ui.GlareCheckBox.setChecked(False)

        if self.ui.boxTuningFilePath.text() != "":
            if os.path.isfile(self.ui.boxTuningFilePath.text()):
                cmd.insert(2, "-a")
                cmd.insert(3, self.ui.boxTuningFilePath.text())

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
            self.printInfo("Decamprof Finish. DCP was create")
            self.oldICCprofile = self.outputICCfilename
            self.createICCFileName(rootname="")
            self.ui.InstallProfile.setEnabled(True)
            PresetManagement.saveAllParams(self.ui, self.CEGATS_path, self.ti3, self.tempFolder, self.outputICCfilename, None)
            self.updateHistoryCombo()
        else:
            self.printInfo("ERROR: DCP was NOT create, check terminal display")



    def runProfCheck(self, output):
        '''
        Run ArgillCMS Profcheck to get delta errors
        :param output:
        :return:
        '''
        executable = os.path.join(self.pathArgyllExecutables, "profcheck")

        cmd = [executable, "-v2", "-Ir", self.ti3, self.outputICCfilename]

        _, proofdata = self.executeTool(cmd, "PROFCHECK", "argyll", output)

        PresetManagement.saveAllParams(self.ui, self.CEGATS_path, self.ti3, self.tempFolder,self.outputICCfilename, proofdata )

        self.loadProofChart(proofdata)
        self.loadProofDELChart(proofdata)
        self.loadProofDECChart(proofdata)
        self.loadProofDEHChart(proofdata)

        self.printInfo("Profcheck finish")


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

        if not copyright:
            copyright = "RoughProfiler By JPereira"

        if not manufacturer:
            manufacturer = "Unknow"

        if not model:
            model = "Unknow"

        if not description:
            description = "None"

        emphasis = self.ui.ArgyllEmphasisSlider.value()
        emphasis = "-V" + str(round(emphasis * 0.1, 1) + 1)

        executable = os.path.join(self.pathArgyllExecutables, "colprof")

        cmd = [executable, "-v", "-a", argyllAlgoritm, "-O",
               self.outputICCfilename, "-A", manufacturer, "-M", model, "-D", description, "-C", copyright,
               os.path.splitext(self.ti3)[0]]

        if self.ui.RemoveB2ATable.isChecked():
            cmd.insert( 4, "-bn")

        if argyllAlgoritm == "l" or argyllAlgoritm == "x":
            cmd.insert(5, argyllUParam)
            cmd.insert(6, emphasis)
            cmd.insert(7, "-q"+argyllRes)

        print(cmd)

        output, _ = self.executeTool(cmd, "COLPROF", "argyll", output="")

        if os.path.isfile(self.outputICCfilename):
            self.printInfo("Colprof finish. ICC was create")
            self.runProfCheck(output)
            self.oldICCprofile = self.outputICCfilename
            self.ui.createProofImage.setEnabled(True)
            self.ui.InstallProfile.setEnabled(True)
            self.createICCFileName(rootname="")
            self.updateHistoryCombo()
        else:
            self.printInfo("ERROR: ICC was NOT create, check terminal display")

    def createdProofimage(self):
        '''
        Create a tiff image form test chart image with the icc profile attached and an letterbox with params info
        :return:
        '''

        if os.path.isfile(self.outputICCfilename):
            icc = self.outputICCfilename
        else:
            icc = self.oldICCprofile

        CreateProofImage(self.inputImage, icc, self.ui, self.tempFolder)

        name_orig, ext_orig = os.path.splitext(os.path.basename(icc))
        file = os.path.join(self.tempFolder, name_orig + ".tiff")

        if os.path.isfile(file):
            AppWarningsClass.informative_warn("Image " + name_orig + ".tiff" + " was create ")
            self.printInfo("Image " + name_orig + ".tiff" + " was create ")

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
            self.printInfo("Raw processing wait a moment")
            QApplication.processEvents()
            linealImage = DevelopImages.raw_lineal_develop(self.rawinputfile)
            #cv2.imwrite(path, linealImage)
            #to save in special characters path
            is_success, im_buf_arr = cv2.imencode(".tiff", linealImage)
            im_buf_arr.tofile(path)

        if os.path.isfile(path):
            self.inputImage = path
            image_data = self.loadImageFromPath(self.inputImage)
            self.linealImageSize = image_data.shape
            self.gamma = "-G1.0"
            return True
        else:
            return AppWarningsClass.critical_warn(
                "Error on raw processing, not linear image")
            self.printInfo("Error on raw processing, not linear image")


    def readImage(self):
        '''
        Read image with ArgyllCMS scanin
        :return:
        '''


        if self.isRaw:
            self.createLinearImage()

        if len(self.coodinates) > 0:
            if self.checkCoordinatesInside():

                executable = os.path.join(self.pathArgyllExecutables, "scanin")


                if not os.path.isfile(self.recogfile) or not os.path.isfile(self.reference):
                    self.printInfo("Recognition file "+self.recogfile+" or reference file"+self.reference+" lost!")
                    return AppWarningsClass.critical_warn("Recognition file "+self.recogfile+" or reference file"+self.reference+" lost!")
                else:

                    # coordinate to string
                    res = []
                    for i in self.coodinates:
                        for j in i:
                            res.append(str(round(j, 2)))
                    coor = ",".join(res)
                    gamma = "-G" + self.config['SCANIN']['gamma']
                    diagnostics = self.config['SCANIN']['diagnostics']

                    cmd = [executable, "-v2","-p", diagnostics, gamma, "-F", coor, "-O", str(self.ti3), str(self.inputImage),
                           str(self.recogfile), str(self.reference), str(self.diag)]


                    #print(" ".join(cmd))
                    self.executeTool(cmd, "SCANIN", "argyll", output="")

                    if os.path.isfile(self.ti3):
                        # enable ICC/DCP buton
                        self.printInfo("Scannin finish, ti3 was create")
                        self.ui.ExecuteTask.setEnabled(True)
                    if os.path.isfile(self.diag):
                        self.printInfo("Scannin finish, diag.tiff was create")
                        # load diag image
                        self.loadDiag()
                        self.ui.tabWidget_2.setTabEnabled(1, True)
                        self.ui.tabWidget_2.setCurrentIndex(1)
                        #PresetManagement.saveCoordinates(self.tempFolder, coor)
            else:
                self.printInfo("There are coordinates outside!")
                return AppWarningsClass.critical_warn("There are coordinates outside!")

        else:
            self.printInfo("Select a region of interest first")
            return AppWarningsClass.critical_warn("Select a region of interest first")

    def executeTool(self, cmd, toolName, workflow, output, **kwargs):
        '''
        Execute binary files
        :param cmd: list of params
        :param toolName: string with name of tool for informative log
        :return:
        '''

        if (os.name == 'nt'):
            # check this params, not run in win10
            kwargs.setdefault('creationflags', subprocess.CREATE_NO_WINDOW)

        self.ui.textEdit.clear()
        proofcheckOutput = []

        if output != "":
            # print(output)
            self.ui.textEdit.insertPlainText(output)

        self.ui.tabWidget_2.setCurrentIndex(2)
        self.ui.tabWidget_2.setTabEnabled(2, True)

        self.ui.textEdit.insertPlainText("---- " + toolName + "-----\n")
        QApplication.processEvents()

        self.printInfo("Running "+toolName+", wait!")
        cmd = list(filter(None, cmd))
        p = subprocess.Popen(cmd, shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             **kwargs)  #creationflags=0x00000008

        #https://stackoverflow.com/questions/1016384/cross-platform-subprocess-with-hidden-window
        #https://stackoverflow.com/questions/74048217/hide-popen-in-exe-mode

        if workflow == "dcamprof":
            output = p.stderr.readline
        elif workflow == "argyll":
            output = p.stdout.readline

        proof = ColorProof()
        for line in iter(output, b''):
            if toolName == "PROFCHECK":
                item = proof.formatProfCheck(line.decode(encoding="utf-8", errors='ignore'))

                proofcheckOutput.append(item)
                self.ui.textEdit.insertPlainText(proof.itemTostring(item))
            else:
                #ISO-8859-1
                txt = line.decode(encoding="utf-8", errors='ignore')
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
            #image_data = cv2.imread(self.diag)
            image_data = self.loadImageFromPath(self.diag)

            if image_data is not None:
                lay_w = self.ui.verticalLayoutWidget_2.frameGeometry().width()
                lay_h = self.ui.verticalLayoutWidget_2.frameGeometry().height()

                image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
                #image_data = image_data.astype(np.uint16)
                image_data, self.factor = self.image_resize(image_data, width=lay_w, height=None, inter=cv2.INTER_AREA)
                image_data = cv2.flip(image_data, 0) # image apear flip in viewBox ¿?
                imageitem = pg.ImageItem(image_data, axisOrder='row-major')

                # clean widgets before
                for i in reversed(range(self.ui.verticalLayout_2.count())):
                    self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)
                graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
                graphicsView.setBackground(QColor(250, 250, 250))
                graphicsView.setObjectName("Diagnostics_file")
                v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
                v2a.setMouseEnabled(x=False, y=False)
                v2a.setLimits(xMin=0, xMax=lay_w)
                v2a.setAspectLocked()
                v2a.disableAutoRange('xy')
                v2a.addItem(imageitem)
                v2a.autoRange()

                self.ui.verticalLayout_2.addWidget(graphicsView)
            else:
                AppWarningsClass.informative_warn("Diag file is corrupt")


    def clearDeltas(self):
        '''
        Clear delta-e, de-C, de-L y de-H graphs after load a new image
        :return:
        '''

        self.ui.tabWidget_2.setTabEnabled(3, False)

        for i in reversed(range(self.ui.verticalLayout_prooftab.count())):
            self.ui.verticalLayout_prooftab.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.verticalLayout_prooftab_DEL.count())):
            self.ui.verticalLayout_prooftab_DEL.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.verticalLayout_prooftab_DEC.count())):
            self.ui.verticalLayout_prooftab_DEC.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.verticalLayout_prooftab_DEH.count())):
            self.ui.verticalLayout_prooftab_DEH.itemAt(i).widget().setParent(None)


    def loadProofChart(self, data):
        '''
        Print Delta-e Chart
        :param data:
        :return:
        '''

        if len(data) > 0:
            delta = round(float(data[-1][0]), 1)
            deltaM = round(float(data[-1][1]), 1)
            self.ui.DeltaEValue.setText(str(delta))
            self.ui.DeltaEValueMax.setText(str(deltaM))

            for i in reversed(range(self.ui.verticalLayout_prooftab.count())):
                self.ui.verticalLayout_prooftab.itemAt(i).widget().setParent(None)

            lay_w = self.ui.verticalLayoutWidget_3.frameGeometry().width()
            lay_h = self.ui.verticalLayoutWidget_3.frameGeometry().height()
            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
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
                colors.append(item[2][:7])
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
        '''
        Print delta-L chart
        :param data:
        :return:
        '''

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEL.count())):
                self.ui.verticalLayout_prooftab_DEL.itemAt(i).widget().setParent(None)

            lay_w = self.ui.verticalLayoutWidget_4.frameGeometry().width()
            lay_h = self.ui.verticalLayoutWidget_4.frameGeometry().height()
            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot_DE')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                xlab.append(float(item[3][0]))
                colors.append(item[2][:7])
                ticks.append((i, item[0]))
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEL.addWidget(window)

    def loadProofDECChart(self, data):
        '''
        Print delta-C Chart
        :param data:
        :return:
        '''

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEC.count())):
                self.ui.verticalLayout_prooftab_DEC.itemAt(i).widget().setParent(None)

            lay_w = self.ui.verticalLayoutWidget_5.frameGeometry().width()
            lay_h = self.ui.verticalLayoutWidget_5.frameGeometry().height()
            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='Plot_DC')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                ticks.append((i, item[0]))
                xlab.append(float(item[3][1]))
                colors.append(item[2][:7])
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEC.addWidget(window)

    def loadProofDEHChart(self, data):
        '''
        Print Delta-H Chart
        :param data:
        :return:
        '''

        if len(data) > 1:
            for i in reversed(range(self.ui.verticalLayout_prooftab_DEH.count())):
                self.ui.verticalLayout_prooftab_DEH.itemAt(i).widget().setParent(None)

            lay_w = self.ui.verticalLayoutWidget_6.frameGeometry().width()
            lay_h = self.ui.verticalLayoutWidget_6.frameGeometry().height()
            graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
            graphicsView.setObjectName("graphicsView")

            window = pg.PlotWidget(name='PlotDH')

            xlab = []
            ticks = []
            colors = []
            i = 0
            for item in data:
                # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
                ticks.append((i, item[0]))
                xlab.append(float(item[3][2]))
                colors.append(item[2][:7])
                i = i + 1

            window.getAxis('bottom').setTicks([ticks])
            bargraph = pg.BarGraphItem(x=range(len(xlab)), height=xlab, width=0.5,
                                       brushes=colors)
            window.addItem(bargraph)
            self.ui.verticalLayout_prooftab_DEH.addWidget(window)

    def loadImageFromPath(self, inputPath):
        '''
        This is neecesary to load images from paths with special chars like spanish language "ñ"
        :param inputPath:
        :return:
        '''
        try:
            stream = open(inputPath, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            return bgrImage
        except Exception as exception:
            self.printInfo("Err Loading File: "+exception)
            AppWarningsClass.critical_warn("Err Loading File: "+exception)


    def loadImage(self):
        '''
        Load proof image on main layout, first tab
        :return:
        '''


        try:
            #image_data = cv2.imread(self.inputImage)
            image_data = self.loadImageFromPath(self.inputImage)
            #get layout size for resize image
            if image_data is not None:
                lay_w = self.ui.verticalLayoutWidget.frameGeometry().width()
                lay_h = self.ui.verticalLayoutWidget.frameGeometry().height()

                self.gammaImageSize = image_data.shape
                image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
                #image_data = image_data.astype(np.uint16)
                image_data, self.factor = self.image_resize(image_data, width=lay_w, height=None, inter=cv2.INTER_AREA)
                pg.setConfigOptions(imageAxisOrder='row-major')
                imageitem = pg.ImageItem(image_data)
                #imageitem.setOpts(axisOrder='row-major')

                # clean widgets before
                for i in reversed(range(self.ui.verticalLayout.count())):
                    self.ui.verticalLayout.itemAt(i).widget().setParent(None)

                graphicsView = pg.GraphicsLayoutWidget(show=True, size=(lay_w, lay_h), border=True)
                graphicsView.setObjectName("test_image")
                graphicsView.setBackground( QColor(250,250,250) )
                v2a = graphicsView.addViewBox(row=0, col=0, lockAspect=True, enableMouse=False)
                v2a.setMouseEnabled(x=False, y=False)
                v2a.setLimits(xMin=0, xMax=lay_w)
                v2a.setAspectLocked()
                v2a.invertY(True)
                v2a.disableAutoRange('xy')
                v2a.addItem(imageitem)
                v2a.addItem(self.createROI())  # load ROI
                v2a.autoRange()
                self.ui.verticalLayout.addWidget(graphicsView)
                self.ui.verticalLayout.update()

                self.printInfo("The image was uploaded")
            else:
                AppWarningsClass.informative_warn("Err Loading File: unknown err ")
                self.printInfo("Err Loading File: unknown err ")

        except cv2.error as e:

            AppWarningsClass.informative_warn("Err Loading File: "+str(e))
            self.printInfo("Err Loading File: "+str(e))

    def createROI(self):
        '''
        Create Region Of Interest
        :return:
        '''
        if os.path.isfile( os.path.join(self.tempFolder, "coordinates.json")  ):
            top_left,bottom_right, self.coodinates = PresetManagement.readCoordinates(self.tempFolder)
        else:
            lay_w = self.ui.verticalLayoutWidget.frameGeometry().width()
            lay_h = self.ui.verticalLayoutWidget.frameGeometry().height()
            centro = [lay_w / 2, lay_h / 2]
            ratio = lay_w / lay_h
            top_left = [centro[0] - self.pad_roi * ratio / 2, centro[1] - self.pad_roi / 2]
            bottom_right = [self.pad_roi * ratio, self.pad_roi]


        my_roi = pg.ROI(top_left, bottom_right , pen=pg.mkPen(width=4.5, color='r'))

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

        return m.T[0].astype(float).item(), m.T[1].astype(float).item()

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

        if w < 600:
            self.printInfo("ROI is too narrow, accuracy may be low")
        elif h > w:
            self.printInfo("Is target in vertical position? This is not going to work! Please check the target position")
        else:
            self.printInfo("")

        top_left = self.rotate_via_numpy((x, y), angle)
        top_right = self.rotate_via_numpy((w + x, y), angle)
        bottom_right = self.rotate_via_numpy((w + x, h + y), angle)
        bottom_left = self.rotate_via_numpy((x, h + y), angle)

        self.coodinates = [top_left, top_right, bottom_right, bottom_left]

        self.createTempFolder()
        PresetManagement.saveCoordinates(self.tempFolder,state, self.coodinates )
        self.checkTargets()
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

        prefix = self.config["OTHERS"]["filenamesufix"]
        if prefix != "":
            prefix = "_"+str(prefix)+"_"

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
        filename = "{0}{1}{2}.{3}".format(rootname,prefix, counter, ext)
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

