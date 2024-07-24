# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RoughProfiler2(object):
    def setupUi(self, RoughProfiler2):
        RoughProfiler2.setObjectName("RoughProfiler2")
        RoughProfiler2.resize(853, 658)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RoughProfiler2.sizePolicy().hasHeightForWidth())
        RoughProfiler2.setSizePolicy(sizePolicy)
        RoughProfiler2.setMinimumSize(QtCore.QSize(0, 0))
        self.OpenImage = QtWidgets.QToolButton(RoughProfiler2)
        self.OpenImage.setGeometry(QtCore.QRect(10, 20, 61, 51))
        self.OpenImage.setObjectName("OpenImage")
        self.LoadCGATS = QtWidgets.QToolButton(RoughProfiler2)
        self.LoadCGATS.setGeometry(QtCore.QRect(10, 80, 61, 51))
        self.LoadCGATS.setObjectName("LoadCGATS")
        self.ReferenceNameValue = QtWidgets.QLabel(RoughProfiler2)
        self.ReferenceNameValue.setGeometry(QtCore.QRect(100, 590, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ReferenceNameValue.setFont(font)
        self.ReferenceNameValue.setStyleSheet("color: rgb(116, 116, 116);")
        self.ReferenceNameValue.setText("")
        self.ReferenceNameValue.setObjectName("ReferenceNameValue")
        self.FileLabel = QtWidgets.QLabel(RoughProfiler2)
        self.FileLabel.setGeometry(QtCore.QRect(20, 570, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FileLabel.setFont(font)
        self.FileLabel.setStyleSheet("color: rgb(116, 116, 116);")
        self.FileLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FileLabel.setObjectName("FileLabel")
        self.ReferenceLabel = QtWidgets.QLabel(RoughProfiler2)
        self.ReferenceLabel.setGeometry(QtCore.QRect(20, 590, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ReferenceLabel.setFont(font)
        self.ReferenceLabel.setStyleSheet("color: rgb(116, 116, 116);")
        self.ReferenceLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ReferenceLabel.setObjectName("ReferenceLabel")
        self.Signature = QtWidgets.QLabel(RoughProfiler2)
        self.Signature.setGeometry(QtCore.QRect(30, 620, 391, 20))
        self.Signature.setStyleSheet("color: rgb(200, 116, 116);")
        self.Signature.setText("")
        self.Signature.setObjectName("Signature")
        self.TargetType = QtWidgets.QComboBox(RoughProfiler2)
        self.TargetType.setGeometry(QtCore.QRect(600, 30, 221, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.TargetType.setFont(font)
        self.TargetType.setStyleSheet("color: rgb(145, 145, 145);")
        self.TargetType.setObjectName("TargetType")
        self.label_4 = QtWidgets.QLabel(RoughProfiler2)
        self.label_4.setGeometry(QtCore.QRect(600, 10, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(155, 155, 155);")
        self.label_4.setObjectName("label_4")
        self.tabWidget = QtWidgets.QTabWidget(RoughProfiler2)
        self.tabWidget.setGeometry(QtCore.QRect(600, 140, 231, 411))
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"  border: 1px solid lightgray;\n"
"  top:5px; \n"
"  background: rgb(240, 240, 240);\n"
"} ")
        self.tabWidget.setObjectName("tabWidget")
        self.ArgyllCM = QtWidgets.QWidget()
        self.ArgyllCM.setObjectName("ArgyllCM")
        self.ProfileResLabel = QtWidgets.QLabel(self.ArgyllCM)
        self.ProfileResLabel.setGeometry(QtCore.QRect(20, 70, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ProfileResLabel.setFont(font)
        self.ProfileResLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.ProfileResLabel.setObjectName("ProfileResLabel")
        self.ArgyllRes = QtWidgets.QComboBox(self.ArgyllCM)
        self.ArgyllRes.setGeometry(QtCore.QRect(20, 90, 191, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ArgyllRes.setFont(font)
        self.ArgyllRes.setStyleSheet("color: rgb(145, 145, 145);")
        self.ArgyllRes.setObjectName("ArgyllRes")
        self.ProfileTypeLabel = QtWidgets.QLabel(self.ArgyllCM)
        self.ProfileTypeLabel.setGeometry(QtCore.QRect(20, 20, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ProfileTypeLabel.setFont(font)
        self.ProfileTypeLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.ProfileTypeLabel.setObjectName("ProfileTypeLabel")
        self.TonalControlLabel = QtWidgets.QLabel(self.ArgyllCM)
        self.TonalControlLabel.setGeometry(QtCore.QRect(20, 120, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TonalControlLabel.setFont(font)
        self.TonalControlLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.TonalControlLabel.setObjectName("TonalControlLabel")
        self.ArgyllAlgoritm = QtWidgets.QComboBox(self.ArgyllCM)
        self.ArgyllAlgoritm.setGeometry(QtCore.QRect(20, 40, 191, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ArgyllAlgoritm.setFont(font)
        self.ArgyllAlgoritm.setStyleSheet("color: rgb(145, 145, 145);")
        self.ArgyllAlgoritm.setObjectName("ArgyllAlgoritm")
        self.ArgyllUparam = QtWidgets.QComboBox(self.ArgyllCM)
        self.ArgyllUparam.setGeometry(QtCore.QRect(20, 140, 191, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ArgyllUparam.setFont(font)
        self.ArgyllUparam.setStyleSheet("color: rgb(145, 145, 145);")
        self.ArgyllUparam.setObjectName("ArgyllUparam")
        self.ARgyllUslicer = QtWidgets.QSlider(self.ArgyllCM)
        self.ARgyllUslicer.setGeometry(QtCore.QRect(20, 190, 151, 22))
        self.ARgyllUslicer.setMinimum(0)
        self.ARgyllUslicer.setMaximum(20)
        self.ARgyllUslicer.setSingleStep(1)
        self.ARgyllUslicer.setProperty("value", 10)
        self.ARgyllUslicer.setSliderPosition(10)
        self.ARgyllUslicer.setOrientation(QtCore.Qt.Horizontal)
        self.ARgyllUslicer.setObjectName("ARgyllUslicer")
        self.ArgyllUscale = QtWidgets.QLabel(self.ArgyllCM)
        self.ArgyllUscale.setGeometry(QtCore.QRect(180, 190, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ArgyllUscale.setFont(font)
        self.ArgyllUscale.setStyleSheet("color: rgb(116, 116, 116);")
        self.ArgyllUscale.setObjectName("ArgyllUscale")
        self.TonalControlLabel_2 = QtWidgets.QLabel(self.ArgyllCM)
        self.TonalControlLabel_2.setGeometry(QtCore.QRect(20, 170, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TonalControlLabel_2.setFont(font)
        self.TonalControlLabel_2.setStyleSheet("color: rgb(155, 155, 155);")
        self.TonalControlLabel_2.setObjectName("TonalControlLabel_2")
        self.ArgyllEmphasisSlider = QtWidgets.QSlider(self.ArgyllCM)
        self.ArgyllEmphasisSlider.setGeometry(QtCore.QRect(20, 250, 160, 22))
        self.ArgyllEmphasisSlider.setMinimum(0)
        self.ArgyllEmphasisSlider.setMaximum(30)
        self.ArgyllEmphasisSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ArgyllEmphasisSlider.setObjectName("ArgyllEmphasisSlider")
        self.TonalControlLabel_3 = QtWidgets.QLabel(self.ArgyllCM)
        self.TonalControlLabel_3.setGeometry(QtCore.QRect(20, 230, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TonalControlLabel_3.setFont(font)
        self.TonalControlLabel_3.setStyleSheet("color: rgb(155, 155, 155);")
        self.TonalControlLabel_3.setObjectName("TonalControlLabel_3")
        self.ArgyllGridEmphasis = QtWidgets.QLabel(self.ArgyllCM)
        self.ArgyllGridEmphasis.setGeometry(QtCore.QRect(190, 250, 21, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ArgyllGridEmphasis.setFont(font)
        self.ArgyllGridEmphasis.setStyleSheet("color: rgb(116, 116, 116);")
        self.ArgyllGridEmphasis.setObjectName("ArgyllGridEmphasis")
        self.tabWidget.addTab(self.ArgyllCM, "")
        self.Dcamprof = QtWidgets.QWidget()
        self.Dcamprof.setObjectName("Dcamprof")
        self.YLimitBox = QtWidgets.QLineEdit(self.Dcamprof)
        self.YLimitBox.setGeometry(QtCore.QRect(30, 270, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.YLimitBox.setFont(font)
        self.YLimitBox.setStyleSheet("color: rgb(145, 145, 145);")
        self.YLimitBox.setObjectName("YLimitBox")
        self.exposureOffsetValue = QtWidgets.QLabel(self.Dcamprof)
        self.exposureOffsetValue.setGeometry(QtCore.QRect(180, 140, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.exposureOffsetValue.setFont(font)
        self.exposureOffsetValue.setStyleSheet("color: rgb(155, 155, 155);")
        self.exposureOffsetValue.setObjectName("exposureOffsetValue")
        self.label_10 = QtWidgets.QLabel(self.Dcamprof)
        self.label_10.setGeometry(QtCore.QRect(20, 120, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(155, 155, 155);")
        self.label_10.setObjectName("label_10")
        self.label_9 = QtWidgets.QLabel(self.Dcamprof)
        self.label_9.setGeometry(QtCore.QRect(20, 20, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(155, 155, 155);")
        self.label_9.setObjectName("label_9")
        self.DcamprofTOPeratoDCP = QtWidgets.QComboBox(self.Dcamprof)
        self.DcamprofTOPeratoDCP.setGeometry(QtCore.QRect(20, 90, 191, 26))
        self.DcamprofTOPeratoDCP.setStyleSheet("color: rgb(145, 145, 145);")
        self.DcamprofTOPeratoDCP.setObjectName("DcamprofTOPeratoDCP")
        self.DcamprofIlluminant = QtWidgets.QComboBox(self.Dcamprof)
        self.DcamprofIlluminant.setGeometry(QtCore.QRect(20, 200, 191, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DcamprofIlluminant.setFont(font)
        self.DcamprofIlluminant.setStyleSheet("color: rgb(145, 145, 145);")
        self.DcamprofIlluminant.setObjectName("DcamprofIlluminant")
        self.GlareCheckBox = QtWidgets.QCheckBox(self.Dcamprof)
        self.GlareCheckBox.setGeometry(QtCore.QRect(20, 240, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.GlareCheckBox.setFont(font)
        self.GlareCheckBox.setStyleSheet("color: rgb(155, 155, 155);")
        self.GlareCheckBox.setObjectName("GlareCheckBox")
        self.LookCorrection = QtWidgets.QCheckBox(self.Dcamprof)
        self.LookCorrection.setGeometry(QtCore.QRect(20, 300, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LookCorrection.setFont(font)
        self.LookCorrection.setStyleSheet("color: rgb(155, 155, 155);")
        self.LookCorrection.setObjectName("LookCorrection")
        self.DcamExposureSlider = QtWidgets.QSlider(self.Dcamprof)
        self.DcamExposureSlider.setGeometry(QtCore.QRect(20, 140, 141, 22))
        self.DcamExposureSlider.setMinimum(-20)
        self.DcamExposureSlider.setMaximum(20)
        self.DcamExposureSlider.setOrientation(QtCore.Qt.Horizontal)
        self.DcamExposureSlider.setObjectName("DcamExposureSlider")
        self.IlluminantLabel = QtWidgets.QLabel(self.Dcamprof)
        self.IlluminantLabel.setGeometry(QtCore.QRect(30, 180, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.IlluminantLabel.setFont(font)
        self.IlluminantLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.IlluminantLabel.setObjectName("IlluminantLabel")
        self.label_8 = QtWidgets.QLabel(self.Dcamprof)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(155, 155, 155);")
        self.label_8.setObjectName("label_8")
        self.DcamprofToneDCP = QtWidgets.QComboBox(self.Dcamprof)
        self.DcamprofToneDCP.setGeometry(QtCore.QRect(20, 40, 191, 26))
        self.DcamprofToneDCP.setStyleSheet("color: rgb(145, 145, 145);")
        self.DcamprofToneDCP.setObjectName("DcamprofToneDCP")
        self.IlluminantLabel_2 = QtWidgets.QLabel(self.Dcamprof)
        self.IlluminantLabel_2.setGeometry(QtCore.QRect(90, 270, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.IlluminantLabel_2.setFont(font)
        self.IlluminantLabel_2.setStyleSheet("color: rgb(155, 155, 155);")
        self.IlluminantLabel_2.setObjectName("IlluminantLabel_2")
        self.tabWidget.addTab(self.Dcamprof, "")
        self.ExecuteTask = QtWidgets.QToolButton(RoughProfiler2)
        self.ExecuteTask.setGeometry(QtCore.QRect(600, 570, 71, 61))
        self.ExecuteTask.setObjectName("ExecuteTask")
        self.ManufacturerText = QtWidgets.QLineEdit(RoughProfiler2)
        self.ManufacturerText.setGeometry(QtCore.QRect(170, 10, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ManufacturerText.setFont(font)
        self.ManufacturerText.setStyleSheet("color: rgb(145, 145, 145);")
        self.ManufacturerText.setObjectName("ManufacturerText")
        self.ModelText = QtWidgets.QLineEdit(RoughProfiler2)
        self.ModelText.setGeometry(QtCore.QRect(170, 50, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ModelText.setFont(font)
        self.ModelText.setStyleSheet("color: rgb(145, 145, 145);")
        self.ModelText.setObjectName("ModelText")
        self.DestText = QtWidgets.QLineEdit(RoughProfiler2)
        self.DestText.setGeometry(QtCore.QRect(170, 90, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.DestText.setFont(font)
        self.DestText.setStyleSheet("color: rgb(145, 145, 145);")
        self.DestText.setObjectName("DestText")
        self.CopyRightText = QtWidgets.QLineEdit(RoughProfiler2)
        self.CopyRightText.setGeometry(QtCore.QRect(310, 10, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.CopyRightText.setFont(font)
        self.CopyRightText.setStyleSheet("color: rgb(145, 145, 145);")
        self.CopyRightText.setObjectName("CopyRightText")
        self.FileNameText = QtWidgets.QLineEdit(RoughProfiler2)
        self.FileNameText.setGeometry(QtCore.QRect(310, 50, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.FileNameText.setFont(font)
        self.FileNameText.setStyleSheet("color: rgb(145, 145, 145);")
        self.FileNameText.setObjectName("FileNameText")
        self.ManufacturerLabel = QtWidgets.QLabel(RoughProfiler2)
        self.ManufacturerLabel.setGeometry(QtCore.QRect(170, 30, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ManufacturerLabel.setFont(font)
        self.ManufacturerLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.ManufacturerLabel.setObjectName("ManufacturerLabel")
        self.DeviceLabel = QtWidgets.QLabel(RoughProfiler2)
        self.DeviceLabel.setGeometry(QtCore.QRect(170, 70, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DeviceLabel.setFont(font)
        self.DeviceLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.DeviceLabel.setObjectName("DeviceLabel")
        self.DescLabel = QtWidgets.QLabel(RoughProfiler2)
        self.DescLabel.setGeometry(QtCore.QRect(170, 110, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DescLabel.setFont(font)
        self.DescLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.DescLabel.setObjectName("DescLabel")
        self.CopyText = QtWidgets.QLabel(RoughProfiler2)
        self.CopyText.setGeometry(QtCore.QRect(310, 30, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CopyText.setFont(font)
        self.CopyText.setStyleSheet("color: rgb(155, 155, 155);")
        self.CopyText.setObjectName("CopyText")
        self.FileNameLabel = QtWidgets.QLabel(RoughProfiler2)
        self.FileNameLabel.setGeometry(QtCore.QRect(310, 70, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.FileNameLabel.setFont(font)
        self.FileNameLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.FileNameLabel.setObjectName("FileNameLabel")
        self.tabWidget_2 = QtWidgets.QTabWidget(RoughProfiler2)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 140, 581, 411))
        self.tabWidget_2.setAutoFillBackground(False)
        self.tabWidget_2.setStyleSheet("QTabWidget::pane {\n"
"  border: 1px solid lightgray;\n"
"  top:5px; \n"
"  background: rgb(240, 240, 240);\n"
"} \n"
"")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.ProofImageTab = QtWidgets.QWidget()
        self.ProofImageTab.setObjectName("ProofImageTab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ProofImageTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 561, 361))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_2.addTab(self.ProofImageTab, "")
        self.RecogImage = QtWidgets.QWidget()
        self.RecogImage.setObjectName("RecogImage")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.RecogImage)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 571, 361))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget_2.addTab(self.RecogImage, "")
        self.Terminal = QtWidgets.QWidget()
        self.Terminal.setObjectName("Terminal")
        self.textEdit = QtWidgets.QTextEdit(self.Terminal)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 561, 361))
        self.textEdit.setObjectName("textEdit")
        self.tabWidget_2.addTab(self.Terminal, "")
        self.proofTab = QtWidgets.QWidget()
        self.proofTab.setObjectName("proofTab")
        self.tabsDeltas = QtWidgets.QTabWidget(self.proofTab)
        self.tabsDeltas.setGeometry(QtCore.QRect(10, 10, 561, 361))
        self.tabsDeltas.setStyleSheet("QTabWidget::pane {\n"
"  border: 0px;\n"
"} ")
        self.tabsDeltas.setObjectName("tabsDeltas")
        self.DEe = QtWidgets.QWidget()
        self.DEe.setObjectName("DEe")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.DEe)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 561, 331))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_prooftab = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_prooftab.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_prooftab.setObjectName("verticalLayout_prooftab")
        self.tabsDeltas.addTab(self.DEe, "")
        self.DEL = QtWidgets.QWidget()
        self.DEL.setObjectName("DEL")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.DEL)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 561, 331))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_prooftab_DEL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_prooftab_DEL.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_prooftab_DEL.setObjectName("verticalLayout_prooftab_DEL")
        self.tabsDeltas.addTab(self.DEL, "")
        self.DEC = QtWidgets.QWidget()
        self.DEC.setObjectName("DEC")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.DEC)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 561, 331))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_prooftab_DEC = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_prooftab_DEC.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_prooftab_DEC.setObjectName("verticalLayout_prooftab_DEC")
        self.tabsDeltas.addTab(self.DEC, "")
        self.DEH = QtWidgets.QWidget()
        self.DEH.setObjectName("DEH")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.DEH)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(0, 0, 561, 331))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_prooftab_DEH = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_prooftab_DEH.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_prooftab_DEH.setObjectName("verticalLayout_prooftab_DEH")
        self.tabsDeltas.addTab(self.DEH, "")
        self.tabWidget_2.addTab(self.proofTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.boxConfArgyll = QtWidgets.QLineEdit(self.tab)
        self.boxConfArgyll.setGeometry(QtCore.QRect(20, 40, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfArgyll.setFont(font)
        self.boxConfArgyll.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfArgyll.setObjectName("boxConfArgyll")
        self.confLabelArgyll = QtWidgets.QLabel(self.tab)
        self.confLabelArgyll.setGeometry(QtCore.QRect(20, 20, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabelArgyll.setFont(font)
        self.confLabelArgyll.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabelArgyll.setObjectName("confLabelArgyll")
        self.boxConfDcamprof = QtWidgets.QLineEdit(self.tab)
        self.boxConfDcamprof.setGeometry(QtCore.QRect(20, 100, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfDcamprof.setFont(font)
        self.boxConfDcamprof.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfDcamprof.setReadOnly(True)
        self.boxConfDcamprof.setObjectName("boxConfDcamprof")
        self.confLabelDcamprof = QtWidgets.QLabel(self.tab)
        self.confLabelDcamprof.setGeometry(QtCore.QRect(20, 80, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabelDcamprof.setFont(font)
        self.confLabelDcamprof.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabelDcamprof.setObjectName("confLabelDcamprof")
        self.OpenArgyllPath = QtWidgets.QPushButton(self.tab)
        self.OpenArgyllPath.setGeometry(QtCore.QRect(400, 31, 113, 41))
        self.OpenArgyllPath.setObjectName("OpenArgyllPath")
        self.openDcamprofPath = QtWidgets.QPushButton(self.tab)
        self.openDcamprofPath.setGeometry(QtCore.QRect(400, 90, 113, 41))
        self.openDcamprofPath.setObjectName("openDcamprofPath")
        self.boxConfICCPath = QtWidgets.QLineEdit(self.tab)
        self.boxConfICCPath.setGeometry(QtCore.QRect(20, 149, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfICCPath.setFont(font)
        self.boxConfICCPath.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfICCPath.setReadOnly(True)
        self.boxConfICCPath.setObjectName("boxConfICCPath")
        self.OpenICCsystemPath = QtWidgets.QPushButton(self.tab)
        self.OpenICCsystemPath.setGeometry(QtCore.QRect(400, 140, 113, 41))
        self.OpenICCsystemPath.setObjectName("OpenICCsystemPath")
        self.confLabelICCPath = QtWidgets.QLabel(self.tab)
        self.confLabelICCPath.setGeometry(QtCore.QRect(20, 129, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabelICCPath.setFont(font)
        self.confLabelICCPath.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabelICCPath.setObjectName("confLabelICCPath")
        self.confLabelICCPath_2 = QtWidgets.QLabel(self.tab)
        self.confLabelICCPath_2.setGeometry(QtCore.QRect(20, 180, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabelICCPath_2.setFont(font)
        self.confLabelICCPath_2.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabelICCPath_2.setObjectName("confLabelICCPath_2")
        self.OpenDCPsistemPath = QtWidgets.QPushButton(self.tab)
        self.OpenDCPsistemPath.setGeometry(QtCore.QRect(400, 190, 113, 41))
        self.OpenDCPsistemPath.setObjectName("OpenDCPsistemPath")
        self.boxConfDCPSystemPath = QtWidgets.QLineEdit(self.tab)
        self.boxConfDCPSystemPath.setGeometry(QtCore.QRect(20, 200, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfDCPSystemPath.setFont(font)
        self.boxConfDCPSystemPath.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfDCPSystemPath.setReadOnly(True)
        self.boxConfDCPSystemPath.setObjectName("boxConfDCPSystemPath")
        self.boxConfCopyright = QtWidgets.QLineEdit(self.tab)
        self.boxConfCopyright.setGeometry(QtCore.QRect(20, 250, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfCopyright.setFont(font)
        self.boxConfCopyright.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfCopyright.setObjectName("boxConfCopyright")
        self.confLabelCopyright = QtWidgets.QLabel(self.tab)
        self.confLabelCopyright.setGeometry(QtCore.QRect(20, 230, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabelCopyright.setFont(font)
        self.confLabelCopyright.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabelCopyright.setObjectName("confLabelCopyright")
        self.SaveCopyright = QtWidgets.QPushButton(self.tab)
        self.SaveCopyright.setGeometry(QtCore.QRect(130, 241, 61, 41))
        self.SaveCopyright.setObjectName("SaveCopyright")
        self.boxConfFilenamePrefix = QtWidgets.QLineEdit(self.tab)
        self.boxConfFilenamePrefix.setGeometry(QtCore.QRect(20, 300, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfFilenamePrefix.setFont(font)
        self.boxConfFilenamePrefix.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfFilenamePrefix.setObjectName("boxConfFilenamePrefix")
        self.confLabeFilePrefix = QtWidgets.QLabel(self.tab)
        self.confLabeFilePrefix.setGeometry(QtCore.QRect(20, 280, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabeFilePrefix.setFont(font)
        self.confLabeFilePrefix.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabeFilePrefix.setObjectName("confLabeFilePrefix")
        self.SaveFilenamePrefix = QtWidgets.QPushButton(self.tab)
        self.SaveFilenamePrefix.setGeometry(QtCore.QRect(130, 290, 61, 41))
        self.SaveFilenamePrefix.setObjectName("SaveFilenamePrefix")
        self.boxConfDefaultModel = QtWidgets.QLineEdit(self.tab)
        self.boxConfDefaultModel.setGeometry(QtCore.QRect(20, 350, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.boxConfDefaultModel.setFont(font)
        self.boxConfDefaultModel.setStyleSheet("color: rgb(145, 145, 145);")
        self.boxConfDefaultModel.setObjectName("boxConfDefaultModel")
        self.confLabeDefaultModel = QtWidgets.QLabel(self.tab)
        self.confLabeDefaultModel.setGeometry(QtCore.QRect(20, 330, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confLabeDefaultModel.setFont(font)
        self.confLabeDefaultModel.setStyleSheet("color: rgb(155, 155, 155);")
        self.confLabeDefaultModel.setObjectName("confLabeDefaultModel")
        self.SaveDefaultModel = QtWidgets.QPushButton(self.tab)
        self.SaveDefaultModel.setGeometry(QtCore.QRect(130, 340, 61, 41))
        self.SaveDefaultModel.setObjectName("SaveDefaultModel")
        self.tabWidget_2.addTab(self.tab, "")
        self.ExecuteReadImage = QtWidgets.QToolButton(RoughProfiler2)
        self.ExecuteReadImage.setGeometry(QtCore.QRect(520, 570, 71, 61))
        self.ExecuteReadImage.setObjectName("ExecuteReadImage")
        self.InstallProfile = QtWidgets.QToolButton(RoughProfiler2)
        self.InstallProfile.setGeometry(QtCore.QRect(680, 570, 71, 61))
        self.InstallProfile.setObjectName("InstallProfile")
        self.createProofImage = QtWidgets.QToolButton(RoughProfiler2)
        self.createProofImage.setGeometry(QtCore.QRect(760, 570, 71, 61))
        self.createProofImage.setObjectName("createProofImage")
        self.FileNameValue = QtWidgets.QLabel(RoughProfiler2)
        self.FileNameValue.setGeometry(QtCore.QRect(100, 570, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FileNameValue.setFont(font)
        self.FileNameValue.setStyleSheet("color: rgb(116, 116, 116);")
        self.FileNameValue.setText("")
        self.FileNameValue.setObjectName("FileNameValue")

        self.retranslateUi(RoughProfiler2)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(4)
        self.tabsDeltas.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RoughProfiler2)

    def retranslateUi(self, RoughProfiler2):
        _translate = QtCore.QCoreApplication.translate
        RoughProfiler2.setWindowTitle(_translate("RoughProfiler2", "RoughProfiler2 by JPEREIRA.net"))
        self.OpenImage.setToolTip(_translate("RoughProfiler2", "Load Image"))
        self.OpenImage.setText(_translate("RoughProfiler2", "..."))
        self.LoadCGATS.setToolTip(_translate("RoughProfiler2", "Load CGATS file"))
        self.LoadCGATS.setText(_translate("RoughProfiler2", "..."))
        self.FileLabel.setText(_translate("RoughProfiler2", "File:"))
        self.ReferenceLabel.setText(_translate("RoughProfiler2", "Reference:"))
        self.label_4.setText(_translate("RoughProfiler2", "Target type"))
        self.ProfileResLabel.setText(_translate("RoughProfiler2", "Profile Resolution"))
        self.ProfileTypeLabel.setText(_translate("RoughProfiler2", "Profile Type"))
        self.TonalControlLabel.setText(_translate("RoughProfiler2", "WP Scale"))
        self.ArgyllUscale.setText(_translate("RoughProfiler2", "0"))
        self.TonalControlLabel_2.setText(_translate("RoughProfiler2", "WP custom Scale"))
        self.TonalControlLabel_3.setText(_translate("RoughProfiler2", "cLUT grid emphasis"))
        self.ArgyllGridEmphasis.setText(_translate("RoughProfiler2", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ArgyllCM), _translate("RoughProfiler2", "ICC"))
        self.YLimitBox.setText(_translate("RoughProfiler2", "−0.2"))
        self.exposureOffsetValue.setText(_translate("RoughProfiler2", "0"))
        self.label_10.setText(_translate("RoughProfiler2", "Exposure Ofset"))
        self.label_9.setText(_translate("RoughProfiler2", "Tone Curve"))
        self.GlareCheckBox.setText(_translate("RoughProfiler2", "Glare Compensation"))
        self.LookCorrection.setText(_translate("RoughProfiler2", "Look corretion"))
        self.IlluminantLabel.setText(_translate("RoughProfiler2", "Illuminant"))
        self.label_8.setText(_translate("RoughProfiler2", "Tone Operator"))
        self.IlluminantLabel_2.setText(_translate("RoughProfiler2", "Y Limit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Dcamprof), _translate("RoughProfiler2", "DCP"))
        self.ExecuteTask.setToolTip(_translate("RoughProfiler2", "Create Profile"))
        self.ExecuteTask.setText(_translate("RoughProfiler2", "..."))
        self.ManufacturerLabel.setText(_translate("RoughProfiler2", "Manufacturer"))
        self.DeviceLabel.setText(_translate("RoughProfiler2", "Device"))
        self.DescLabel.setText(_translate("RoughProfiler2", "Description"))
        self.CopyText.setText(_translate("RoughProfiler2", "Copyright"))
        self.FileNameLabel.setText(_translate("RoughProfiler2", "Filename"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.ProofImageTab), _translate("RoughProfiler2", "Proof Image"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.RecogImage), _translate("RoughProfiler2", "Recog Image"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.Terminal), _translate("RoughProfiler2", "Terminal"))
        self.tabsDeltas.setTabText(self.tabsDeltas.indexOf(self.DEe), _translate("RoughProfiler2", "DE-e"))
        self.tabsDeltas.setTabText(self.tabsDeltas.indexOf(self.DEL), _translate("RoughProfiler2", "DE-L"))
        self.tabsDeltas.setTabText(self.tabsDeltas.indexOf(self.DEC), _translate("RoughProfiler2", "DE-C"))
        self.tabsDeltas.setTabText(self.tabsDeltas.indexOf(self.DEH), _translate("RoughProfiler2", "DE-H"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.proofTab), _translate("RoughProfiler2", "Proof"))
        self.confLabelArgyll.setText(_translate("RoughProfiler2", "ArgyllCMS Excecutalbles"))
        self.confLabelDcamprof.setText(_translate("RoughProfiler2", "Dcamprof Excecutalbles"))
        self.OpenArgyllPath.setText(_translate("RoughProfiler2", "Open"))
        self.openDcamprofPath.setText(_translate("RoughProfiler2", "Open"))
        self.OpenICCsystemPath.setText(_translate("RoughProfiler2", "Open"))
        self.confLabelICCPath.setText(_translate("RoughProfiler2", "ICC System Folder"))
        self.confLabelICCPath_2.setText(_translate("RoughProfiler2", "DCP System Folder"))
        self.OpenDCPsistemPath.setText(_translate("RoughProfiler2", "Open"))
        self.confLabelCopyright.setText(_translate("RoughProfiler2", "Copyright"))
        self.SaveCopyright.setText(_translate("RoughProfiler2", "Save"))
        self.confLabeFilePrefix.setText(_translate("RoughProfiler2", "Filename Prefix"))
        self.SaveFilenamePrefix.setText(_translate("RoughProfiler2", "Save"))
        self.confLabeDefaultModel.setText(_translate("RoughProfiler2", "Default Model"))
        self.SaveDefaultModel.setText(_translate("RoughProfiler2", "Save"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), _translate("RoughProfiler2", "Conf"))
        self.ExecuteReadImage.setToolTip(_translate("RoughProfiler2", "Read Image"))
        self.ExecuteReadImage.setText(_translate("RoughProfiler2", "..."))
        self.InstallProfile.setToolTip(_translate("RoughProfiler2", "Install Profile"))
        self.InstallProfile.setText(_translate("RoughProfiler2", "..."))
        self.createProofImage.setToolTip(_translate("RoughProfiler2", "Create Proof Image"))
        self.createProofImage.setText(_translate("RoughProfiler2", "..."))

