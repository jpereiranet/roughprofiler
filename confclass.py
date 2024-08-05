
import configparser
import os.path
from app_paths import DefinePathsClass
import glob
from warning_class import AppWarningsClass
import shutil

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
    def getuserpaths(ui):

        user = os.getlogin()

        if os.name == 'posix':
            icc = os.path.join("/Users", user,"Library/ColorSync/Profiles/")
            dcp = os.path.join("/Users", user,"Library/Application Support/Adobe/CameraRaw/CameraProfiles")
        else:
            icc = os.path.join("C:/Windows/System32/spool/drivers/color")
            dcp = os.path.join("C:/Users/",user,"/AppData/Roaming/Adobe/CameraRaw/CameraProfiles")

        config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        config.read(path_conf_file)

        ui.boxConfCopyright.setText(user)
        config['OTHERS']['copyright'] = user

        if os.path.isdir(icc):
            ui.boxConfICCPath.setText(icc)
            config['INSTALL']['PATHICC'] = icc
            if os.path.isdir(dcp):
                config['INSTALL']['PATHDCP'] = dcp
                ui.boxConfDCPSystemPath.setText(dcp)

        with open(path_conf_file, 'w') as configfile:
            config.write(configfile)



    @staticmethod
    def programsAutoPath(ui):
        '''
        if folder "programs" exists with the Argyll and Dcamprof tools, paths are auto-configured
        :param ui:
        :return:
        '''
        program_paths = DefinePathsClass.create_programs_paths()

        if os.path.isdir(program_paths):
            config = configparser.ConfigParser()
            path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
            config.read(path_conf_file)
            config['APPS']['ARGYLL'] = program_paths
            ui.boxConfArgyll.setText(program_paths)
            ui.boxConfArgyll.repaint()
            config['APPS']['DCAMPROF'] = program_paths
            ui.boxConfDcamprof.setText(program_paths)
            ui.boxConfDcamprof.repaint()
            ui.OpenImage.setEnabled(True)
            with open(path_conf_file, 'w') as configfile:  # save
                config.write(configfile)

            if (os.name == 'posix'):
                if not os.path.isfile("/usr/local/lib/libomp.dylib"):
                    orig = os.path.join( program_paths,"libomp.dylib")
                    dest = "/usr/local/lib/libomp.dylib"
                    if os.path.isfile( orig ):
                        if AppWarningsClass.informative_true_false("libomp.dylib was not detected on /usr/local/lib. We will try to copy it to your system"):
                            shutil.copyfile(orig, dest)
                            if os.path.isfile(dest):
                                AppWarningsClass.informative_warn("libomp.dylib was copied to /usr/local/lib")
                            else:
                                AppWarningsClass.critical_warn("libomp.dylib was NOT copied to /usr/local/lib")
                    else:
                        AppWarningsClass.informative_warn("You must copy libomp.dylib on /usr/local/lib to run Dcamprof tools")

            return True
        else:
            return False

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


