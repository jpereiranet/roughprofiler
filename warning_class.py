from PyQt5 import QtWidgets


class AppWarningsClass():

    @staticmethod
    def critical_warn(msgI):
        msgboxwarning = QtWidgets.QMessageBox()
        msgboxwarning.setIcon(QtWidgets.QMessageBox.Critical)
        msgboxwarning.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgboxwarning.setText("Error info")
        msgboxwarning.setInformativeText(msgI)
        ret = msgboxwarning.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            return False

    @staticmethod
    def just_warn(msgI):
        msgboxwarning = QtWidgets.QMessageBox()
        msgboxwarning.setIcon(QtWidgets.QMessageBox.Warning)
        msgboxwarning.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgboxwarning.setText("Error info")
        msgboxwarning.setInformativeText(msgI)
        ret = msgboxwarning.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            return False

    @staticmethod
    def informative_warn(msgI):
        msgboxwarning = QtWidgets.QMessageBox()
        msgboxwarning.setIcon(QtWidgets.QMessageBox.Information)
        msgboxwarning.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgboxwarning.setText("Information")
        msgboxwarning.setInformativeText(msgI)
        ret = msgboxwarning.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            return True

    @staticmethod
    def status_warn(msgI):
        msgboxwarning = QtWidgets.QMessageBox()
        msgboxwarning.setIcon(QtWidgets.QMessageBox.Information)
        msgboxwarning.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgboxwarning.setText("Status")
        msgboxwarning.setInformativeText(msgI)
        ret = msgboxwarning.exec_()

    @staticmethod
    def informative_true_false(msgI):
        msgboxwarning = QtWidgets.QMessageBox()
        msgboxwarning.setIcon(QtWidgets.QMessageBox.Information)
        msgboxwarning.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgboxwarning.setText("Information")
        msgboxwarning.setInformativeText(msgI)
        ret = msgboxwarning.exec_()
        if ret == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False
