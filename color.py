from colormath.color_objects import LabColor, sRGBColor, LCHabColor, AdobeRGBColor
from colormath.color_conversions import convert_color
import  json


class ColorProof():


    def __init__(self):

        cadena = "[28.743221] C04: 0.91445260 0.77353450 0.09066738 -> 75.494139 3.148460 109.012936 should be 83.885368 2.642543 81.526502"
        #print( self.formatProfCheck(cadena) )


    def formatProfCheck(self, cadena):
        arr = cadena.split(" ")
        if arr[0] == "No":
            return ""
        elif arr[0] == "Profile":
            return  arr[9].replace(",",""), arr[6].replace(",","")
        else:
            patch = arr[1].replace(":", "")
            delta = round( float( arr[0].replace("]", "").replace("[", "")),1)
            hex = self.convertLabtoHex(arr[11], arr[12], arr[13])
            lch_r = self.convertLabtoLCH(arr[11], arr[12], arr[13])
            lch_s = self.convertLabtoLCH(arr[6], arr[7], arr[8])
            deLCH = self.deltaLCH(lch_r, lch_s)

            RGB_r = self.convertLabtoRGB(arr[11], arr[12], arr[13])
            RGB_s = self.convertLabtoRGB(arr[6], arr[7], arr[8])

            deRGB = self.deRGB(RGB_r, RGB_s)

            return patch, \
                   delta, \
                   hex, \
                   deLCH, \
                   deRGB


    def itemTostring(self, items):

        if len(items) == 2: #es delta y max delta
            return "Delta-e: "+str(items[0]) +" Max: "+str(items[1])+"\n"
        elif len(items) > 2: #son parches
            return items[0] +": "+ str(items[1]) +"\n"


    def convertLabtoHex(self, L, a, b):
        lab = LabColor(L, a, b)
        RGB = convert_color(lab, sRGBColor)
        hex = RGB.get_rgb_hex()
        return hex

    def convertLabtoLCH(self, L, a, b):
        lab = LabColor(L, a, b)
        LCH = convert_color(lab, LCHabColor)
        return LCH


    def deltaLCH(self, lch_r, lch_s):

        deL = round(lch_r.lch_l - lch_s.lch_l,2)
        deC = round(lch_r.lch_c - lch_s.lch_c,2)
        deH = round(lch_r.lch_h - lch_s.lch_h,2)

        return deL, deC, deH

    def convertLabtoRGB(self, L, a, b):
        lab = LabColor(L, a, b)
        RGB = convert_color(lab, AdobeRGBColor)
        return RGB

    def deRGB(self, RGB_r, RGB_s):
        de_R = round( (RGB_r.rgb_r - RGB_s.rgb_r), 1)
        de_G = round( (RGB_r.rgb_g - RGB_s.rgb_g), 1)
        de_B = round( (RGB_r.rgb_b - RGB_s.rgb_b), 1)

        return de_R, de_G, de_B

    def createJson(self, data):
        #print(data)
        l = []

        for item in data:
            # ('A01', 1.0, '#775243', (-0.69, 0.76, -0.25), (-0.4, -0.8, -0.9)),
            l.append( {"Name": item[0], "ScaleRGB": item[4]} )

        json_str = json.dumps(l)
        #print(json_str)

if __name__ == '__main__':

    a = ColorProof()