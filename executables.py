import subprocess
import sys


class executables:

    def __init__(self):
        x = ""

    def runScanin(self, cmd):
        out = ""
        err = ""
        errcode = ""

        process = subprocess.Popen(cmd, shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        out, err = process.communicate()
        errcode = process.returncode

        return out, err, errcode