import math
import os.path
import cv2
import numpy as np
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

        self.loadProofImageParams()
        self.icc = icc
        self.img_cv2 = cv2.imread(img)
        self.ui = ui
        self.tempFolder = tempFolder

        arr = self.readValues()
        w, h = self.letterBox(len(arr))
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

    def loadProofImageParams(self):
        section = "PROOF_IMAGE"
        self.proof_band_ratio = self.readProofParam(section, "band_ratio", 0.12, float, 0.08, 0.25)
        self.proof_min_band_px = self.readProofParam(section, "min_band_px", 90, int, 40, 300)
        self.proof_text_rows = self.readProofParam(section, "text_rows", 4, int, 2, 8)
        self.proof_min_font_scale = self.readProofParam(section, "min_font_scale", 0.38, float, 0.20, 2.0)
        self.proof_max_font_scale = self.readProofParam(section, "max_font_scale", 0.82, float, 0.30, 2.0)
        self.proof_margin_x_ratio = self.readProofParam(section, "margin_x_ratio", 0.025, float, 0.005, 0.10)
        self.proof_margin_y_ratio = self.readProofParam(section, "margin_y_ratio", 0.18, float, 0.05, 0.35)
        self.proof_column_gap_ratio = self.readProofParam(section, "column_gap_ratio", 0.025, float, 0.005, 0.10)
        self.proof_background_color = (230, 241, 232)
        self.proof_text_color = (25, 30, 36)

    def readProofParam(self, section, key, default, cast, min_value, max_value):
        try:
            if not self.config.has_option(section, key):
                return default
            value = cast(self.config.get(section, key))
            return max(min_value, min(max_value, value))
        except (ValueError, TypeError):
            return default

    def letterBox(self, entry_count=0):

        h, w, ch = self.img_cv2.shape
        rows = min(self.proof_text_rows, max(1, entry_count))
        band_height = int(max(self.proof_min_band_px, h * self.proof_band_ratio))
        min_content_height = rows * 24 + 22
        band_height = max(band_height, min_content_height)
        max_band_height = max(min_content_height, int(h * 0.35))
        band_height = min(band_height, max_band_height)

        self.pos = h
        band = np.full((band_height, w, ch), self.proof_background_color, dtype=self.img_cv2.dtype)
        self.img_cv2 = np.vstack((self.img_cv2, band))
        self.img_cv2 = cv2.line(self.img_cv2, (0, self.pos), (w, self.pos), (155, 174, 160), 1)
        return w, h + band_height

    def printText(self, arr, w, h):

        entries = [str(value[0]) + ": " + str(value[1]) for value in arr.values()]
        if not entries:
            return

        font = cv2.FONT_HERSHEY_SIMPLEX
        band_height = h - self.pos
        margin_x = max(12, int(w * self.proof_margin_x_ratio))
        margin_y = max(8, int(band_height * self.proof_margin_y_ratio))
        gap_x = max(18, int(w * self.proof_column_gap_ratio))
        available_w = max(1, w - margin_x * 2)
        available_h = max(1, band_height - margin_y * 2)

        rows = min(self.proof_text_rows, len(entries))
        columns = max(1, math.ceil(len(entries) / rows))
        column_width = max(1, int((available_w - gap_x * (columns - 1)) / columns))

        font_scale = self.computeFontScale(entries, column_width, available_h, rows, font)
        thickness = max(1, int(round(font_scale * 1.5)))
        line_height = available_h / rows

        for index, text in enumerate(entries):
            column = index // rows
            row = index % rows
            fitted_text = self.fitTextToWidth(text, column_width, font, font_scale, thickness)
            text_size = cv2.getTextSize(fitted_text, font, font_scale, thickness)[0]

            x = margin_x + column * (column_width + gap_x)
            y = int(self.pos + margin_y + row * line_height + (line_height + text_size[1]) / 2)
            y = min(h - margin_y, max(self.pos + margin_y + text_size[1], y))

            cv2.putText(self.img_cv2, fitted_text, (x, y), font, font_scale, self.proof_text_color, thickness,
                        cv2.LINE_AA)

    def computeFontScale(self, entries, column_width, available_h, rows, font):
        max_scale_by_height = available_h / max(1, rows * 28)
        font_scale = min(self.proof_max_font_scale, max_scale_by_height)
        font_scale = max(self.proof_min_font_scale, font_scale)

        while font_scale > self.proof_min_font_scale:
            thickness = max(1, int(round(font_scale * 1.5)))
            line_heights = [
                cv2.getTextSize(text, font, font_scale, thickness)[0][1]
                for text in entries
            ]
            if max(line_heights, default=0) <= available_h / rows * 0.75:
                return font_scale
            font_scale -= 0.04

        return self.proof_min_font_scale

    def fitTextToWidth(self, text, max_width, font, font_scale, thickness):
        if cv2.getTextSize(text, font, font_scale, thickness)[0][0] <= max_width:
            return text

        suffix = "..."
        low = 0
        high = len(text)
        best = suffix

        while low <= high:
            middle = (low + high) // 2
            candidate = text[:middle].rstrip() + suffix
            candidate_width = cv2.getTextSize(candidate, font, font_scale, thickness)[0][0]

            if candidate_width <= max_width:
                best = candidate
                low = middle + 1
            else:
                high = middle - 1

        return best

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
