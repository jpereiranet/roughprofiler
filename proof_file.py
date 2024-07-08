import os.path
import cv2
from PIL import Image, ImageCms
import configparser
from app_paths import DefinePathsClass
import json


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


        self.letterBox()
        arr = self.readValues()
        self.printText(arr)
        self.saveImage()

    def readValues(self):

        #self.ui.radioButton
        #self.ui.radioButton_2

        argyllAlgoritm =  list(self.ArgyllAlgoritm)[self.ui.ArgyllAlgoritm.currentIndex()]
        argyllRes =list(self.ArgyllRes)[self.ui.ArgyllRes.currentIndex()]
        argyllUParam = list(self.ArgyllUParam)[self.ui.ArgyllUparam.currentIndex()]

        ArgyllUscale = self.ui.ArgyllUscale.text()
        ArgyllGridEmphasis = self.ui.ArgyllGridEmphasis.text()

        arr = {"ArgyllAlgoritms": (self.ui.ProfileTypeLabel.text(), argyllAlgoritm),
               "ArgyllRes": ("Profile Resolution", argyllRes),
               "ArgyllUparam": ("WP Scale", argyllUParam),
               "ArgyllUscale": ("WP custom Scale", ArgyllUscale),
               "ArgyllGridEmphasis": ("cLUT grid emphasis", ArgyllGridEmphasis)
               }
        return arr


    def letterBox(self):

        h, w, ch = self.img_cv2.shape
        self.pos = int(h / 1.1)
        self.img_cv2 = cv2.rectangle(self.img_cv2, (0, self.pos), (w, h), (0, 255, 0), -1)

    def printText(self, arr):

        i = 0
        c = 0
        rows = 2
        colDisplacement = 600
        margin_top = 70
        padding_y = 20
        margin_left = 50
        fontScale = 2
        thickness = 5

        for value in arr.values():
            if i > rows:
                i = 1
                c = c + 1
            else:
                i = i + 1

            posicion = (margin_left + colDisplacement * c, padding_y + self.pos + margin_top * i)

            campo = value[0] + ": " + value[1]
            cv2.putText(self.img_cv2, campo, posicion, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 0), thickness,
                        cv2.LINE_AA)

            # textsize = cv2.getTextSize(campo, cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)[0]
            # print(textsize)

    def saveImage(self  ):

        name_orig, ext_orig = os.path.splitext( os.path.basename(self.icc) )

        file = os.path.join(self.tempFolder, name_orig+".tiff" )
        profile = ImageCms.getOpenProfile(self.icc)
        img_pil = Image.fromarray(cv2.cvtColor(self.img_cv2, cv2.COLOR_BGR2RGB))
        img_pil.save(file, icc_profile=profile.tobytes())


#if __name__ == '__main__':

    #a = CreateProofImage()