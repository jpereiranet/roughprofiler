
import configparser
from app_paths import DefinePathsClass

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
    def openAndSavePaths( field, value, ui):

        config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")

        config.read(path_conf_file)
        #print(config['DEFAULT']['path'])  # -> "/path/name/"

        if field == "argyllpath":
            ui.boxConfArgyll.setText(value)
            ui.OpenArgyllPath.setText("saved!")
            config['APPS']['ARGYLL'] = value
        if field == "dcamppath":
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

        with open(path_conf_file, 'w') as configfile:  # save
            config.write(configfile)


