



class params:

    @staticmethod
    def targets():
        return {
                   "Colorchecker Classic": ("ColorChecker.cie","ColorChecker.cht", "cc24-layout.json" ),
                   "Colorchecker SG": ("ColorCheckerSG.cie", "ColorCheckerSG.cht", "ccsg-layout.json"),
                   "Colorchecker Passport": ("ColorCheckerPassport.cie", "ColorCheckerPassport.cht", ""),
                   "Colorchecker SG": ("", "ColorCheckerDC.cht", "")
                   }

    @staticmethod
    def ArgyllResolutions():
        return {
                        "Low": "l",
                        "Medium": "m",
                        "High": "h",
                        "Ultra": "u"
                        }

    @staticmethod
    def ArgyllAlgoritms():
        return {
                    "Lab cLUT": "l",
                    "XYZ cLUT": "x",
                    "Gamma+matrix": "g",
                    "Shaper+matrix": "s",
                    "Matrix only": "m",
                    "Single gamma+matrix": "G",
                    "Single shaper+matrix": "S"
                    }

    @staticmethod
    def ArgyllUparam():
        return {
            "clip cLUT values": "-uc",
            "Auto scale WP": "-u",
            "Force Absolute": "-ua",
            "None": "",
            "Custom": ""
        }





