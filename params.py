



class params:

    def __init__(self):

        self.targets = {
                   "Colorchecker Classic": ("ColorChecker.cie","ColorChecker.cht" ),
                   "Colorchecker SG": ("ColorCheckerSG.cie", "ColorCheckerSG.cht"),
                   "Colorchecker Passport": ("ColorCheckerPassport.cie", "ColorCheckerPassport.cht"),
                   "Colorchecker SG": ("", "ColorCheckerDC.cht")
                   }

        self.ArgyllResolutions = {
                            "Low": "l",
                            "Medium": "m",
                            "High": "h",
                            "Ultra": "u"
                            }

        self.ArgyllAlgoritms = {
                            "Lab cLUT": "l",
                            "XYZ cLUT": "x",
                            "Gamma+matrix": "g",
                            "Shaper+matrix": "s",
                            "Matrix only": "m",
                            "Single gamma+matrix": "G",
                            "Single shaper+matrix": "S"
                            }

        self.ArgyllUparam = {
            "clip cLUT values": "-uc",
            "Auto scale WP": "-u",
            "Force Absolute": "-ua",
            "None": "",
            "Custom": ""

        }





