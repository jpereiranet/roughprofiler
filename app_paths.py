import os
import sys


class DefinePathsClass:

    @staticmethod
    def create_resource_path(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        path_icon = os.path.join(application_path, "line-icons", fn)
        return path_icon

    @staticmethod
    def create_reference_paths(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        subpath = ""
        path_icon = os.path.join(application_path, subpath, "reference", fn)

        return path_icon

    @staticmethod
    def create_configuration_paths(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        subpath = ""
        path_icon = os.path.join(application_path, subpath, "configuration", fn)

        return path_icon

    @staticmethod
    def create_programs_paths():

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        path_programs = os.path.join(application_path, "programs")

        return path_programs