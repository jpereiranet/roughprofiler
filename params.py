



class params:

    def __init__(self):

        self.targets = {
                   "Colorchecker Classic": ("ColorChecker.cie","ColorChecker.cht" ),
                   "Colorchecker SG": ("ColorCheckerSG.cie", "ColorCheckerSG.cht"),
                   "Colorchecker Passport": ("ColorCheckerPassport.cie", "ColorCheckerPassport.cht"),
                   "Colorchecker SG": ("", "ColorCheckerDC.cht")
                   }

        self.ArgyllResolutions = {
                            "Low": "-q l",
                            "Medium": "-q m",
                            "High": "-q h",
                            "Ultra": "-q u"
                            }

        self.ArgyllAlgoritms = {
                            "Lab cLUT": "-a l",
                            "XYZ cLUT": "-a x",
                            "Gamma+matrix": "-a g",
                            "Shaper+matrix": "-a s",
                            "Matrix only": "-a m",
                            "Single gamma+matrix": "-a G",
                            "Single shaper+matrix": "-a S"
                            }

        self.ArgyllUparam = {
            "Auto scale WP": "-u",
            "Force Absolute": "-ua",
            "clip cLUT values": "-uc"
        }





