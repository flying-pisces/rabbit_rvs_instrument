import clr
import os
import json
import time
import pprint
import asyncio

def printFormatted(s):
    pprint.pprint(json.loads(s))

clr.AddReference("System")
import System

apiPath = os.path.join(r"C:\Program Files\Radiant Vision Systems\TrueTest 1.7\MPK_API.dll")

clr.AddReference(apiPath)
from MPK_API_CS import *

class MPKtest():
    def __init__(self, verbose = True):
        self._verbose = verbose
        self._device = MPK_API()
        self._databasePath = r"C:\Radiant Vision Systems Data\TrueTest\UserData\Demo.ttxm"
        self._sequencePath = r"C:\Radiant Vision Systems Data\TrueTest\UserData\Demo Sequence.seqx"
        self._exportPath = r"C:\Radiant Vision Systems Data\TrueTest\UserData\\"
        self._exportFileName = r"ExportTest.csv"

    ########################
    # INITIALIZATION
    ########################
    def initializeCamera(self, sn):
        result = self._device.InitializeCamera(sn, False, False)
        if self._verbose:
            printFormatted(result)

    def setDatabase(self):
        result = self._device.SetMeasurementDatabase(self._databasePath)
        if self._verbose:
            printFormatted(result)

    def createDatabase(self):
        result = self._device.CreateMeasurementDatabase(self._databasePath)
        if self._verbose:
            printFormatted(result)
    def setSequence(self):
        result = self._device.SetSequence(self._sequencePath)
        if self._verbose:
            printFormatted(result)

    ########################
    # MEASUREMENT OPERATIONS
    ########################
    def getMeasurementList(self):
        result = self._device.GetMeasurementList()
        if self._verbose:
            printFormatted(result)

    def getNameOfFirstMeasurement(self):
        result = self._device.GetMeasurementList()
        measurementDictList = json.loads(result)
        return measurementDictList[0]['Description']

    def getIDofFirstMeasurement(self):
        result = self._device.GetMeasurementList()
        measurementTuple = json.loads(result)
        return measurementTuple[0]['Measurement ID']

    def getMeasurementInfo(self, imageName):
        result = self._device.GetMeasurementInfo(imageName)
        if self._verbose:
            printFormatted(result)

    def editMeasurementInfo(self, imageName, jsonMeasInfo):
        result = self._device.EditMeasurementInfo(imageName, jsonMeasInfo)
        if self._verbose:
            printFormatted(result)

    def exportMeasurement(self, imageName):
        result = self._device.ExportMeasurement(imageName, self._exportPath, self._exportFileName)
        if self._verbose:
            print(result)
            # printFormatted(result)

    def exportMeasurementAndResize(self, imageName, resX, resY):
        result = self._device.ExportMeasurement(imageName, self._exportPath, self._exportFileName, resX, resY)
        if self._verbose:
            print(result)
    ########################
    # SEQUENCING
    ########################
    def sequenceRunAll(self):
        result = self._device.RunAllSequenceSteps()
        if self._verbose:
            printFormatted(result)

    def sequenceRunAllWithCamera(self, useCamera, saveImages):
        result = self._device.RunAllSequenceSteps(useCamera, saveImages)
        if self._verbose:
            printFormatted(result)

    def sequenceRunStep(self, step):
        result = self._device.RunSequenceStepByName(step)
        if self._verbose:
            printFormatted(result)
            #printFormatted(result)

    def sequenceRunStepList(self, stepList):
        result = self._device.RunSequenceStepListByName(stepList)
        if self._verbose:
            printFormatted(result)
            # printFormatted(result)

    def sequenceStop(self):
        result = self._device.SequenceStop()
        if self._verbose:
            printFormatted(result)

if __name__ == "__main__":
    verbose = True

    testSequencing = False
    testMeasurementOperations = False
    testMeasurementInfoEdit = False
    testExport = True

    device = MPKtest(verbose)
    device._databasePath = r"C:\Radiant Vision Systems Data\TrueTest\UserData\ConoscopeTest.ttxm"
    device._sequencePath = r"C:\Radiant Vision Systems Data\TrueTest\UserData\Demo Sequence.seqx"

    device.initializeCamera("Demo")
    device.setDatabase()
    device.setSequence()

    if testSequencing:
        useCamera = True
        saveMeasurements = True
        device.sequenceRunAll()
        # device.sequenceRunAllWithCamera(useCamera, saveMeasurements)
        # device.sequenceRunStep("ANSI Brightness")
        # device.sequenceRunStepList(["Gradient", "ANSI Brightness"])

    if testMeasurementOperations:
        device.getMeasurementList()
        ID = device.getIDofFirstMeasurement()
        device.getMeasurementInfo(ID)

    if testMeasurementInfoEdit:
        measurementInfoDict = {
            "Description" : "New Description",
            "Model Number" : "New Model Number",
            "Technician" : "New Technician",
            "Pattern" : "New Pattern",
            "Measurement Setup" : "New Measurement Setup"
        }

        device.getMeasurementList()
        ID = device.getIDOfFirstMeasurement()
        device.getMeasurementInfo(ID)

        device.editMeasurementInfo(ID, json.dumps(measurementInfoDict))
        device.getMeasurementInfo(ID)

    if testExport:
        name = device.getNameOfFirstMeasurement()
        device._exportPath = r"C:\Radiant Vision Systems Data\TrueTest\UserData"
        device._exportFileName = r"ExportTest.csv"
        device.exportMeasurementAndResize(name, 100, 100)
        # device._exportFileName = r"ExportTest.png"
        # device.exportMeasurement(name)
        # device._exportFileName = r"ExportTest.jpg"
        # device.exportMeasurement(name)
        # device._exportFileName = r"ExportTest.bmp"
        # device.exportMeasurement(name)
        # device._exportFileName = r"ExportTest1"
        # device.exportMeasurement(name)
        # device._exportFileName = ""
        # device.exportMeasurement(name)

