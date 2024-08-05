import math
import os.path
import cv2
from PIL import Image, ImageCms
import configparser
from app_paths import DefinePathsClass
import json
from warning_class import AppWarningsClass


class CreateProofImage():

    def __init__(self, img, icc, ui, tempFolder):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        if os.path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.ArgyllRes = json.loads(self.config.get('PARAMS', 'ARGYLLRES'))
            self.ArgyllAlgoritm = json.loads(self.config.get('PARAMS', 'ARGYLLALGORITM'))
            self.ArgyllUParam = json.loads(self.config.get('PARAMS', 'ARGYLLUPARAM'))
            self.Targets = json.loads(self.config.get('PARAMS', 'TARGETS'))

        self.icc = icc
        self.img_cv2 = cv2.imread(img)
        self.ui = ui
        self.tempFolder = tempFolder

        w, h = self.letterBox()
        arr = self.readValues()
        self.printText(arr, w, h)
        self.saveImage()

    def readValues(self):

        #index = self.ui.tabsDcamprof.currentIndex()

        #algoritm = self.DcamICCAlgoritm[ list(self.DcamICCAlgoritm)[self.ui.DcamprofAlgortimICC.currentIndex()] ]

        index = self.ui.tabWidget.currentIndex()
        if index == 1:
            #not in use
            arr = {
                    "Engine":("Engine", "Dcamproof"),
                    "DcamprofAlgortimICC": ( "Profile Type", list(self.DcamICCAlgoritm)[self.ui.DcamprofAlgortimICC.currentIndex()]),
                    "DcamprofToneICC": ("Curve", list(self.DcamToneOperator)[self.ui.DcamprofTOPeratorICC.currentIndex()]),
                    "DcamprofTOPeratorICC": ("Operator", list(self.DcamToneCurveICC)[self.ui.DcamprofToneICC.currentIndex()] ),
                    "Illuminant": ("Illuminant", list(self.DcamIlluminant)[self.ui.DcamprofIlluminant.currentIndex()] ),
                    "LUTRes": ("Profile Resolution", self.ICCLutResolution[
                       list(self.ICCLutResolution)[self.ui.DcamprofICCResLUT.currentIndex()]]),
                    "Ylimit": ("Y Limit", self.ui.YLimitBox.text() )

                    }

        elif index == 0:

            arr = {"Engine":("Engine", "Argyll"),
                   "ArgyllAlgoritms": (self.ui.ProfileTypeLabel.text(), list(self.ArgyllAlgoritm)[self.ui.ArgyllAlgoritm.currentIndex()] ),
                   "ArgyllRes": ("Profile Resolution", list(self.ArgyllRes)[self.ui.ArgyllRes.currentIndex()]),
                   "ArgyllUparam": ("WP Scale", list(self.ArgyllUParam)[self.ui.ArgyllUparam.currentIndex()]),
                   "ArgyllUscale": ("WP custom Scale", self.ui.ArgyllUscale.text()),
                   "ArgyllGridEmphasis": ("cLUT grid emphasis", self.ui.ArgyllGridEmphasis.text()),
                   "ICCFileName": ("ICC Filename", self.ui.FileNameText.text()),
                   "Reference": ("Reference", self.ui.ReferenceNameValue.text())
                   }
        return arr


    def letterBox(self):

        h, w, ch = self.img_cv2.shape
        self.pos = int(h / 1.1)
        self.img_cv2 = cv2.rectangle(self.img_cv2, (0, self.pos), (w, h), (0, 255, 0), -1)
        return w, h

    def printText(self, arr, w, h):

        fscale = math.ceil( min(w,h) / 2500 )

        i = 0
        c = 0
        rows = 2
        colDisplacement = math.floor(450 * fscale)
        margin_top = math.floor(35 * fscale)
        padding_y = math.floor(10 * fscale)
        margin_left = 50
        fontScale = fscale
        thickness = math.floor(2.5 * fscale)

        for value in arr.values():
            if i > rows:
                i = 1
                c = c + 1
            else:
                i = i + 1

            posicion = (margin_left + colDisplacement * c, padding_y + self.pos + margin_top * i)

            campo = str(value[0]) + ": " + str(value[1])
            cv2.putText(self.img_cv2, campo, posicion, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 0), thickness,
                        cv2.LINE_AA)

            # textsize = cv2.getTextSize(campo, cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)[0]
            # print(textsize)

    def saveImage(self  ):

        if os.path.isfile(self.icc):
            name_orig, ext_orig = os.path.splitext( os.path.basename(self.icc) )
            file = os.path.join(self.tempFolder, name_orig+".tiff" )
            profile = ImageCms.getOpenProfile(self.icc)
            img_pil = Image.fromarray(cv2.cvtColor(self.img_cv2, cv2.COLOR_BGR2RGB))
            img_pil.save(file, icc_profile=profile.tobytes())
        else:
            AppWarningsClass.informative_warn("ICC Profile LOST!")


#if __name__ == '__main__':

    #a = CreateProofImage()