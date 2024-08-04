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
    def saveAllParams(ui, CGATS, ti3, tempFolder, profilename, proofdata):

        params = {
        "process": ui.tabWidget.currentIndex(),
        "profilename": profilename,
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
        "RemoveB2ATable": ui.RemoveB2ATable.isChecked(),

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
        "YLimitBox": ui.YLimitBox.text(),
        "proofdata": proofdata
        }


        filename = os.path.splitext(ui.FileNameText.text())[0] + ".json"
        pathJson = os.path.join(tempFolder,filename)
        with open(pathJson, "w") as outfile:
            json.dump(params, outfile)

    @staticmethod
    def saveCoordinates(tempFolder, state, coordinates):

        #print(state)
        params = {
            "x": state['pos'][0],
            "y": state['pos'][1],
            "w": state['size'][0],
            "h": state['size'][1],
            "angle": state['angle'],
            "coordinates": coordinates
        }

        pathJson = os.path.join(tempFolder,"coordinates.json")

        with open(pathJson, "w") as outfile:
            json.dump(params, outfile)

    @staticmethod
    def readCoordinates(tempFolder):

        file = os.path.join(tempFolder, "coordinates.json")
        if os.path.isfile(file):
            f = open(file)
            data = json.load(f)
            return [ data["x"], data["y"] ], [data["w"], data["h"] ], data["coordinates"]


    @staticmethod
    def populateHistoryCombo(tempFolder):

        files = glob.glob(os.path.join(tempFolder, "*.json"))
        baseName = os.path.basename(tempFolder)
        files.sort(key=os.path.getmtime)
        f = ["---"]
        for file in files:
            baseNameFile = os.path.splitext(os.path.basename(file))[0] #remove dcamprof json from list
            if baseNameFile != baseName and baseNameFile != "coordinates":
                f.append( baseNameFile )
        return f



    @staticmethod
    def readLastPreset(ui, tempFolder):

        files = glob.glob(os.path.join(tempFolder, "*.json"))
        files.sort(key=os.path.getmtime)
        if len(files) > 0:
            last = files[-1]
            PresetManagement.setParams(ui,last )

    @staticmethod
    def checkHashFiles(file, hash, param):
        if file:
            if PresetManagement.sha256sum(file) != hash:
                AppWarningsClass.informative_warn(param+" file are changed since this preset was made")


    @staticmethod
    def setParams(ui,file):

        f = open(file)
        data = json.load(f)

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
        ui.RemoveB2ATable.setChecked(data["RemoveB2ATable"])

        ui.ManufacturerText.setText(data["ManufacturerText"] )
        ui.ManufacturerText.repaint()
        ui.CopyRightText.setText(data["CopyRightText"] )
        ui.CopyRightText.repaint()
        ui.ModelText.setText(data["ModelText"] )
        ui.ModelText.repaint()
        #ui.FileNameText.setText(data["FileNameText"] )
        #ui.DestText.setText(data["DestText"] )

        ui.DcamprofToneDCP.setCurrentIndex(data["DcamprofToneDCP"])
        ui.DcamprofTOPeratoDCP.setCurrentIndex(data["DcamprofTOPeratoDCP"])
        ui.exposureOffsetValue.setText( data["exposureOffsetValue"])
        ui.DcamExposureSlider.setValue( int( round(float(data["exposureOffsetValue"])*10,0) ))
        ui.DcamprofIlluminant.setCurrentIndex(data["DcamprofIlluminant"])
        ui.GlareCheckBox.setChecked( data["GlareCheckBox"] )
        ui.YLimitBox.setText( data["YLimitBox"] )

        return data
