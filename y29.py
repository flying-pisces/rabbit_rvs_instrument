import os
import json
import clr
clr.AddReference('System.Drawing')
apipath = os.path.join(os.getcwd(), "MPK_API.dll")
clr.AddReference(apipath)
from MPK_API import *
from System.Drawing import *
from System import String
from datetime import datetime

class Y29Error():
    pass

class Y29():
    def __init__(self, verbose=False, focus_distance=0.49, lens_aperture=8.0, auto_exposure=True, rect=[0, 0, 0, 0]):
        self.name = "y29"
        self._verbose = verbose
        self._device = MPK_API()
        self._error_message = self.name + "is out of work"
        self._read_error = False
        self._focus_distance = focus_distance; #dimension of m
        self._lens_aperture = lens_aperture;
        self._auto_exposure = auto_exposure;
        self._rect = rect;
        
    def timestamp(self):
        return str(datetime.now())
        
    def serialnumber(self): 
        response = self._device.GetCameraSerial()
        snjson = json.loads(str(response))
        sn = str(snjson.values())
        if self._verbose:
            print(sn)
        return sn
    
    def version(self): 
        response = self._device.GetApiVersionInfo()
        versionjson = json.loads(str(response))
        versioninfo = str(versionjson.values())
        if self._verbose:
            print(versionjson)
        return versioninfo
    
    def init(self, sn):
        response = self._device.InitializeCamera(sn, False, True)
        initjson = json.loads(str(response))
        initvalue = str(initjson.values())
        if self._verbose:
            print(initvalue)
        return initvalue
#####################################################################################################
######### Measurement Setup ##################
    # CreateMeasurementSetup(patternName as String, redEFilterxposure as Single, greenFilterExposure as Single,
#                       blueFilterExposure as Single, xbFilterExposure as Single, focusDistance as Single,
#                       lenAperture as Single, autoAdjustExposure as Boolean, subframeRegion as Rectangle) 
    def measurementsetup(self, pattern="photopic", eR = 100, eG = 100, eB = 100, eXB = 100):
        meas_setup = self._device.CreateMeasurementSetup(pattern,
                                           eR, eG, eB, eXB,
                                           self._focus_distance,
                                           self._lens_aperture,
                                           self._auto_exposure ,
                                           self._rect)
        response = int(str(String.Format("Measurement Setup Result for " + pattern +" - ErrorCode: {0}", meas_setup['ErrorCode'])).split(":")[1])
        if self._verbose:
            print response
        return response 
#colorCals = mpkapi.GetColorCalibrationList()
#print('Color Cals:')
#print(colorCals)
    def getcolorcalibrationlist(self):
        response = str(self._device.GetColorCalibrationList()).replace('\r\n', '')
        colorcalibrationlistjson = json.loads(response)
        colorcalibrationlistid = colorcalibrationlistjson.keys()
        if self._verbose:
            print colorcalibrationlistjson
        return colorcalibrationlistid
    
    def getcolorshiftcalibrationlist(self):
        response = str(self._device.GetColorShiftCalibrationList()).replace('\r\n', '')
        colorshiftcalibrationlistjson = json.loads(response)
        colorshiftcalibrationlistid = colorshiftcalibrationlistjson.keys()
        if self._verbose:
            print colorshiftcalibrationlistjson
        return colorshiftcalibrationlistid
    
    def getimagescalecalibrationlist(self):
        response = str(self._device.GetImageScaleCalibrationList()).replace('\r\n', '')
        imagescalecalibrationlistjson = json.loads(response)
        imagescalecalibrationlistid = imagescalecalibrationlistjson.keys()
        if self._verbose:
            print imagescalecalibrationlistjson
        return imagescalecalibrationlistid

    def getflatfieldcalibrationlist(self):
        response = str(self._device.GetFlatFieldCalibrationList()).replace('\r\n', '')
        flatfieldcalibrationlistjson = json.loads(response)
        flatfieldcalibrationlistid = flatfieldcalibrationlistjson.keys()
        if self._verbose:
            print flatfieldcalibrationlistjson
        return flatfieldcalibrationlistid


######################
#SetCalibration(measurementSetupName As String, colorCalibrationID As Integer, imageScaleID As Integer, colorShiftID As Integer)

#setwhitecalibration = mpkapi.SetCalibrations("White", 20, 3, 4)
#print('Set Calibrations for White')
#print(setwhitecalibration)

    def setcalibrationid(self, meassetup, colorcalibrationid, imagescaleid, colorshiftid):
        response = self._device.SetCalibrations(meassetup, colorcalibrationid, imagescaleid, colorshiftid)
        if self._verbose:
            print(response)


#resultSN1 = mpkapi.SetSerialNumber("SN1", 0)
#print('Serial 1 Set')
#print(resultSN1)
    def setsn(self, sn, channel=0):
        response = self._device.SetSerialNumber(sn, channel)
        if self._verbose:
            print(response)

#getSerialResult1 = mpkapi.ReadSerialNumbers(0)
#print(getSerialResult1)
            
    def getsn(self, channel=0):
        response = self._device.ReadSerialNumber(channel)
        if self._verbose:
            print(response)
#####################################################################################################
## Camera Control

# CaptureMeasurement(measurementSetupName as String, imageKey as String, saveToDatabase as Boolean)
    def capture(self, pattern, imagekey="photopickey", SaveToDatabase = False):
        response = self._device.CaptureMeasurement(pattern, imagekey, SaveToDatabase)
        if self._verbose:
            print(String.Format("Measurement Capture Result for " + pattern + " - Image Key: {0}", response['Imagekey']))
        

#####################################################################################################
## Image Analysis

#result = mpkapi.PrepareForRun()
#print(String.Format("Prepare For Run - ErrorCode: {0}", result['ErrorCode']))
    def prepareanalysis(self):
        response = str(self._device.PrepareForRun).replace('\r\n', '')
        prepareforrunjson = json.loads(response)
        isprepareforrun = "0" in prepareforrunjson.values()
        if self._verbose:
            print(response)
        return isprepareforrun
            
    def focusvalue(self):
        response = str(self._device.GetFocusMetric().replace('\r\n', ''))
        focusjson = json.loads(response)
        value = int(focusjson.values())
        return value

    def export(imagekey, directory = "C:\\oculus\\Monterey_Cleanroom_Stations\\rvs_instrument\\Data"):
        response = self._device.ExportData(imagekey, directory)
        
        
        pass
        
        
    #################################################################################
## ExportData(ImageKey as String)
#exportdata = mpkapi.ExportData("SN_TIME_W", "C:\Radiant Vision Systems Data", "W_Image")
#print(String.Format("Export Data Result for White - ErrorCode: {0}", result['ErrorCode']))
'''
exportdata = mpkapi.ExportData("SN_TIME_R", "C:\\oculus\\Tuzi_Cleanroom_Stations\\CV1TestAndFactory\\TestExec\\\thirdparty\\radiant\\Data")
print(String.Format("Export Data Result for Red - ErrorCode: {0}", result['ErrorCode']))
'''

        

if __name__ == "__main__":
    verbose=True
    focus_distance=0.49
    lens_aperture=8.0
    auto_exposure=False
    cx = 953 #Left
    cy = 505 #Top
    cl = 4586 #Width
    cw = 3879 #Height
    rect = Rectangle(cx, cy, cl, cw)
    the_instrument = Y29(verbose, focus_distance, lens_aperture, auto_exposure, rect)
    sn = the_instrument.serialnumber()
    isinit = the_instrument.init(sn)
    version = the_instrument.version()
    
    the_instrument.measurementsetup("White", 120, 120, 120, 120)

    the_instrument.getcolorcalibrationlist() #11
    the_instrument.getcolorshiftcalibrationlist() #6
    the_instrument.getimagescalecalibrationlist() #3
    the_instrument.getflatfieldcalibrationlist() #6
    
    meassetup = "White"
    colorcalibrationid = 2
    imagescaleid = 1
    colorshiftid = 0
    the_instrument.setcalibrationid(meassetup, colorcalibrationid, imagescaleid, colorshiftid) 

    pattern = "white"
    ts = the_instrument.timestamp()
    imagekey = ''.join([ts, '_', pattern])# can be set by end user. Prefer to set product_SN_YYMMDDHHMMSS    
    isSavetoDatabase = True
    the_instrument.capture(meassetup, imagekey, isSavetoDatabase)
    
    isanalysisready = the_instrument.prepareanalysis()
    fv = the_instrument.focusvalue()
    


    

  
  