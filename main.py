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
        RoughProfiler2.resize(853, 642)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RoughProfiler2.sizePolicy().hasHeightForWidth())
        RoughProfiler2.setSizePolicy(sizePolicy)
        self.OpenImage = QtWidgets.QToolButton(RoughProfiler2)
        self.OpenImage.setGeometry(QtCore.QRect(10, 20, 61, 51))
        self.OpenImage.setObjectName("OpenImage")
        self.LoadCGATS = QtWidgets.QToolButton(RoughProfiler2)
        self.LoadCGATS.setGeometry(QtCore.QRect(10, 80, 61, 51))
        self.LoadCGATS.setObjectName("LoadCGATS")
        self.FileNameValue = QtWidgets.QLabel(RoughProfiler2)
        self.FileNameValue.setGeometry(QtCore.QRect(100, 570, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FileNameValue.setFont(font)
        self.FileNameValue.setStyleSheet("color: rgb(116, 116, 116);")
        self.FileNameValue.setText("")
        self.FileNameValue.setObjectName("FileNameValue")
        self.ReferenceNameValue = QtWidgets.QLabel(RoughProfiler2)
        self.ReferenceNameValue.setGeometry(QtCore.QRect(100, 590, 221, 16))
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
        self.Signature.setGeometry(QtCore.QRect(30, 610, 591, 20))
        self.Signature.setObjectName("Signature")
        self.TargetType = QtWidgets.QComboBox(RoughProfiler2)
        self.TargetType.setGeometry(QtCore.QRect(600, 30, 221, 26))
        self.TargetType.setObjectName("TargetType")
        self.label_4 = QtWidgets.QLabel(RoughProfiler2)
        self.label_4.setGeometry(QtCore.QRect(600, 10, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(155, 155, 155);")
        self.label_4.setObjectName("label_4")
        self.tabWidget = QtWidgets.QTabWidget(RoughProfiler2)
        self.tabWidget.setGeometry(QtCore.QRect(600, 140, 231, 351))
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
        self.ArgyllAlgoritm.setObjectName("ArgyllAlgoritm")
        self.ArgyllUparam = QtWidgets.QComboBox(self.ArgyllCM)
        self.ArgyllUparam.setGeometry(QtCore.QRect(20, 140, 191, 26))
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
        self.IlluminantLabel = QtWidgets.QLabel(self.Dcamprof)
        self.IlluminantLabel.setGeometry(QtCore.QRect(10, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.IlluminantLabel.setFont(font)
        self.IlluminantLabel.setStyleSheet("color: rgb(155, 155, 155);")
        self.IlluminantLabel.setObjectName("IlluminantLabel")
        self.DcamprofIlluminant = QtWidgets.QComboBox(self.Dcamprof)
        self.DcamprofIlluminant.setGeometry(QtCore.QRect(10, 60, 191, 26))
        self.DcamprofIlluminant.setObjectName("DcamprofIlluminant")
        self.DcamprofICC = QtWidgets.QRadioButton(self.Dcamprof)
        self.DcamprofICC.setGeometry(QtCore.QRect(40, 10, 51, 20))
        self.DcamprofICC.setObjectName("DcamprofICC")
        self.DcamprofDCP = QtWidgets.QRadioButton(self.Dcamprof)
        self.DcamprofDCP.setGeometry(QtCore.QRect(120, 10, 61, 20))
        self.DcamprofDCP.setObjectName("DcamprofDCP")
        self.tabWidget.addTab(self.Dcamprof, "")
        self.ExecuteTask = QtWidgets.QToolButton(RoughProfiler2)
        self.ExecuteTask.setGeometry(QtCore.QRect(680, 500, 71, 51))
        self.ExecuteTask.setObjectName("ExecuteTask")
        self.ManufacturerText = QtWidgets.QLineEdit(RoughProfiler2)
        self.ManufacturerText.setGeometry(QtCore.QRect(170, 10, 113, 21))
        self.ManufacturerText.setObjectName("ManufacturerText")
        self.ModelText = QtWidgets.QLineEdit(RoughProfiler2)
        self.ModelText.setGeometry(QtCore.QRect(170, 50, 113, 21))
        self.ModelText.setObjectName("ModelText")
        self.DestText = QtWidgets.QLineEdit(RoughProfiler2)
        self.DestText.setGeometry(QtCore.QRect(170, 90, 291, 21))
        self.DestText.setObjectName("DestText")
        self.CopyRightText = QtWidgets.QLineEdit(RoughProfiler2)
        self.CopyRightText.setGeometry(QtCore.QRect(310, 10, 151, 21))
        self.CopyRightText.setObjectName("CopyRightText")
        self.FileNameText = QtWidgets.QLineEdit(RoughProfiler2)
        self.FileNameText.setGeometry(QtCore.QRect(310, 50, 151, 21))
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
        self.ConfButon = QtWidgets.QToolButton(RoughProfiler2)
        self.ConfButon.setGeometry(QtCore.QRect(80, 20, 61, 51))
        self.ConfButon.setObjectName("ConfButon")
        self.radioButton = QtWidgets.QRadioButton(RoughProfiler2)
        self.radioButton.setGeometry(QtCore.QRect(600, 60, 211, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(RoughProfiler2)
        self.radioButton_2.setGeometry(QtCore.QRect(600, 90, 211, 20))
        self.radioButton_2.setObjectName("radioButton_2")
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
        self.ExecuteReadImage = QtWidgets.QToolButton(RoughProfiler2)
        self.ExecuteReadImage.setGeometry(QtCore.QRect(600, 500, 71, 51))
        self.ExecuteReadImage.setObjectName("ExecuteReadImage")
        self.InstallProfile = QtWidgets.QToolButton(RoughProfiler2)
        self.InstallProfile.setGeometry(QtCore.QRect(760, 500, 71, 51))
        self.InstallProfile.setObjectName("InstallProfile")

        self.retranslateUi(RoughProfiler2)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RoughProfiler2)

    def retranslateUi(self, RoughProfiler2):
        _translate = QtCore.QCoreApplication.translate
        RoughProfiler2.setWindowTitle(_translate("RoughProfiler2", "RoughProfiler2"))
        self.OpenImage.setText(_translate("RoughProfiler2", "..."))
        self.LoadCGATS.setText(_translate("RoughProfiler2", "..."))
        self.FileLabel.setText(_translate("RoughProfiler2", "File:"))
        self.ReferenceLabel.setText(_translate("RoughProfiler2", "Reference:"))
        self.Signature.setText(_translate("RoughProfiler2", "TextLabel"))
        self.label_4.setText(_translate("RoughProfiler2", "Target type"))
        self.ProfileResLabel.setText(_translate("RoughProfiler2", "Profile Resolution"))
        self.ProfileTypeLabel.setText(_translate("RoughProfiler2", "Profile Type"))
        self.TonalControlLabel.setText(_translate("RoughProfiler2", "WP Scale"))
        self.ArgyllUscale.setText(_translate("RoughProfiler2", "0"))
        self.TonalControlLabel_2.setText(_translate("RoughProfiler2", "WP custom Scale"))
        self.TonalControlLabel_3.setText(_translate("RoughProfiler2", "cLUT grid emphasis"))
        self.ArgyllGridEmphasis.setText(_translate("RoughProfiler2", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ArgyllCM), _translate("RoughProfiler2", "Argyll"))
        self.IlluminantLabel.setText(_translate("RoughProfiler2", "Illuminant"))
        self.DcamprofICC.setText(_translate("RoughProfiler2", "ICC"))
        self.DcamprofDCP.setText(_translate("RoughProfiler2", "DCP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Dcamprof), _translate("RoughProfiler2", "Dcamprof"))
        self.ExecuteTask.setText(_translate("RoughProfiler2", "..."))
        self.ManufacturerLabel.setText(_translate("RoughProfiler2", "Manufacturer"))
        self.DeviceLabel.setText(_translate("RoughProfiler2", "Device"))
        self.DescLabel.setText(_translate("RoughProfiler2", "Description"))
        self.CopyText.setText(_translate("RoughProfiler2", "Copyright"))
        self.FileNameLabel.setText(_translate("RoughProfiler2", "Filename"))
        self.ConfButon.setText(_translate("RoughProfiler2", "..."))
        self.radioButton.setText(_translate("RoughProfiler2", "Argyll Workflow (ICC)"))
        self.radioButton_2.setText(_translate("RoughProfiler2", "Dcamprof Workflow (DCP/ICC)"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.ProofImageTab), _translate("RoughProfiler2", "Proof Image"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.RecogImage), _translate("RoughProfiler2", "Recog Image"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.Terminal), _translate("RoughProfiler2", "Terminal"))
        self.ExecuteReadImage.setText(_translate("RoughProfiler2", "..."))
        self.InstallProfile.setText(_translate("RoughProfiler2", "..."))

