
import configparser
import os.path
from app_paths import DefinePathsClass
import glob
from warning_class import AppWarningsClass

class ConfIni():

    @staticmethod
    def saveParams(field, ui):
        config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        config.read(path_conf_file)

        if field == "copyright":
            ui.SaveCopyright.setText("saved!")
            ui.CopyRightText.setText(ui.boxConfCopyright.text())
            config['OTHERS']['copyright'] = ui.boxConfCopyright.text()

        if field == "prefix":
            ui.SaveFilenamePrefix.setText("saved!")
            config['OTHERS']['filenamesufix'] = ui.boxConfFilenamePrefix.text()

        if field == "model":
            ui.SaveCopyright.setText("saved!")
            config['OTHERS']['devicemodel'] = ui.boxConfDefaultModel.text()

        with open(path_conf_file, 'w') as configfile:  # save
            config.write(configfile)


    @staticmethod
    def savelastpath(path):
        config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        config.read(path_conf_file)
        config['PATHS']['lastfolder'] = path
        with open(path_conf_file, 'w') as configfile:  # save
            config.write(configfile)

    @staticmethod
    def openAndSavePaths( field, value, ui):

        std = False
        config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")

        config.read(path_conf_file)

        if field == "argyllpath":
            if not glob.glob(os.path.join( value, "scanin*" )) or not glob.glob(os.path.join(value, "colprof*")) or not glob.glob(os.path.join(value, "profcheck*")):
                AppWarningsClass.critical_warn("Argyll programs are missing on this folder")
                ui.boxConfArgyll.setText("")
                ui.OpenArgyllPath.setText("Open!")
                config['APPS']['ARGYLL'] = ""
            else:
                ui.boxConfArgyll.setText(value)
                ui.OpenArgyllPath.setText("saved!")
                config['APPS']['ARGYLL'] = value
        if field == "dcamppath":
            if not glob.glob(os.path.join( value, "dcamprof*" )):
                AppWarningsClass.critical_warn("Dcamprof program is missing on this folder")
                ui.boxConfDcamprof.setText("")
                ui.openDcamprofPath.setText("Open")
                config['APPS']['DCAMPROF'] = ""
            else:
                ui.boxConfDcamprof.setText(value)
                ui.openDcamprofPath.setText("saved!")
                config['APPS']['DCAMPROF'] = value
        if field == "iccpath":
            ui.OpenICCsystemPath.setText("saved!")
            ui.boxConfICCPath.setText(value)
            config['INSTALL']['PATHICC'] = value
        if field == "dcppath":
            ui.OpenDCPsistemPath.setText("saved!")
            ui.boxConfDCPSystemPath.setText(value)
            config['INSTALL']['PATHDCP'] = value

        with open(path_conf_file, 'r+') as configfile:  # save
            std = True
            config.write(configfile)

        return std


