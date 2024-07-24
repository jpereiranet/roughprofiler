import os.path
import json
import glob
import hashlib
from warning_class import AppWarningsClass

class PresetManagement():


    @staticmethod
    def sha256sum(filename):
        if filename:
            return hashlib.md5(open(filename, 'rb').read()).hexdigest()
        else:
            return filename



    @staticmethod
    def saveAllParams(ui, CGATS, ti3, tempFolder):
        print(ti3)
        print(CGATS)

        params = {
        "process": ui.tabWidget.currentIndex(),
        "ti3": ti3,
        "hash_ti3": PresetManagement.sha256sum(ti3),
        "CEGATS_path": CGATS,
        "CEGATS_hash": PresetManagement.sha256sum(CGATS),
        "TargetType": ui.TargetType.currentIndex(),
        "ArgyllAlgoritm": ui.ArgyllAlgoritm.currentIndex(),
        "ArgyllRes": ui.ArgyllRes.currentIndex(),
        "ArgyllUparam": ui.ArgyllUparam.currentIndex(),
        "ArgyllUscale": ui.ArgyllUscale.text(),
        "ArgyllGridEmphasis": ui.ArgyllGridEmphasis.text(),

        "ManufacturerText": ui.ManufacturerText.text(),
        "CopyRightText": ui.CopyRightText.text(),
        "ModelText": ui.ModelText.text(),
        "FileNameText": ui.FileNameText.text(),
        "DestText": ui.DestText.text(),

        "DcamprofToneDCP": ui.DcamprofToneDCP.currentIndex(),
        "DcamprofTOPeratoDCP": ui.DcamprofTOPeratoDCP.currentIndex(),
        "exposureOffsetValue": ui.exposureOffsetValue.text(),
        "DcamprofIlluminant": ui.DcamprofIlluminant.currentIndex(),
        "GlareCheckBox": ui.GlareCheckBox.isChecked(),
        "YLimitBox": ui.YLimitBox.text()
        }


        filename = os.path.splitext(ui.FileNameText.text())[0] + ".json"
        pathJson = os.path.join(tempFolder,filename)
        with open(pathJson, "w") as outfile:
            json.dump(params, outfile)

    @staticmethod
    def readLastPreset(tempFolder):

        files = glob.glob(os.path.join(tempFolder, "*.json"))
        files.sort(key=os.path.getmtime)
        last = files[-1]
        f = open(last)
        data = json.load(f)
        return data

    @staticmethod
    def checkHashFiles(file, hash, param):
        if file:
            if PresetManagement.sha256sum(file) != hash:
                AppWarningsClass.informative_warn(param+" file are changed since this preset was made")


    @staticmethod
    def setParams(ui,tempFolder ):

        data = PresetManagement.readLastPreset(tempFolder)

        PresetManagement.checkHashFiles(data["ti3"], data["hash_ti3"], "Ti3")
        if data["CEGATS_path"]:
            ui.ReferenceNameValue.setText(os.path.basename(data["CEGATS_path"]))
            PresetManagement.checkHashFiles(data["CEGATS_path"], data["CEGATS_hash"], "CGATS")

        ui.TargetType.setCurrentIndex(data["TargetType"] )
        ui.ArgyllAlgoritm.setCurrentIndex(data["ArgyllAlgoritm"] )
        ui.ArgyllRes.setCurrentIndex(data["ArgyllRes"] )
        ui.ArgyllUparam.setCurrentIndex(data["ArgyllUparam"] )
        ui.ARgyllUslicer.setValue( int( round(float(data["ArgyllUscale"]) / 0.1, 0) ) )
        ui.ArgyllUscale.setText(data["ArgyllUscale"])
        ui.ArgyllEmphasisSlider.setValue(  int(round(float(data["ArgyllGridEmphasis"]) / 0.1, 0 )) )
        ui.ArgyllGridEmphasis.setText(data["ArgyllGridEmphasis"])

        ui.ManufacturerText.setText(data["ManufacturerText"] )
        ui.CopyRightText.setText(data["CopyRightText"] )
        ui.ModelText.setText(data["ModelText"] )
        #ui.FileNameText.setText(data["FileNameText"] )
        #ui.DestText.setText(data["DestText"] )

        ui.DcamprofToneDCP.setCurrentIndex(data["DcamprofToneDCP"])
        ui.DcamprofTOPeratoDCP.setCurrentIndex(data["DcamprofTOPeratoDCP"])
        ui.exposureOffsetValue.setText( data["exposureOffsetValue"])
        ui.DcamExposureSlider.setValue( int( round(float(data["exposureOffsetValue"])*10,0) ))
        ui.DcamprofIlluminant.setCurrentIndex(data["DcamprofIlluminant"])
        ui.GlareCheckBox.setChecked( data["GlareCheckBox"] )
        ui.YLimitBox.setText( data["YLimitBox"] )


if __name__ == '__main__':

    tempFolder  ="/Users/jpereira/Python/roughprofiler2/test/DSC_4453a/"
    PresetManagement.readLastPreset(tempFolder)