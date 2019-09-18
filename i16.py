import os
import json
import clr
clr.AddReference('System.Drawing')
apipath = os.path.join(os.getcwd(), "MPK_API.dll")
clr.AddReference(apipath)
from MPK_API import *
from System.Drawing import *
from System import String

class I16Error():
    pass

class I16():
    def __init__(self, verbose=False, focus_distance=0.5, lens_aperture=2.8, auto_exposure=True, rect=[0, 0, 0, 0]):
        self.name = "i16"
        self._verbose = verbose
        self._device = MPK_API()
        self._error_message = self.name + "is out of work"
        self._read_error = False
        self._focus_distance = focus_distance; #dimension of m
        self._lens_aperture = lens_aperture;
        self._auto_exposure = auto_exposure;
        self._rect = rect;
     
    def serialnumber(self): 
        response = str(self._device.GetCameraSerial())
	responsejson = json.loads(response)
	sn = str(responsejson.values()[0].rstrip())
        if self._verbose:
            print(sn)
        return sn
    
    def tt_version(self): 
        response = self._device.GetTrueTestApiVersionInfo()
        versionjson = json.loads(str(response))
        versioninfo = str(versionjson.values())
        if self._verbose:
            print(versionjson)
        return versioninfo
    
    def mpkapi_version(self): 
        response = self._device.GetMpkApiVersionInfo()
        versionjson = json.loads(str(response))
        versioninfo = str(versionjson.values())
        if self._verbose:
            print(versionjson)
        return versioninfo
    
    def init(self, sn):
        response = self._device.InitializeCamera(sn, False, True)
        init_result = int(str(String.Format("Init Camera Result - ErrorCode: {0}", response['ErrorCode'])).split(":")[1]) # 0 means return successful
        if self._verbose:
            print(init_result)
        return init_result
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

    def is_ready(self): 
        response = str(self._device.EquipmentReady())
        responsejson = json.loads(response)
        is_response_bool = True if str(responsejson.values()[0]) == '0' else False
	return is_response_bool

    def close_comm(self): 
        response = str(self._device.CloseCommunication())
        responsejson = json.loads(response)
        is_response_bool = True if str(responsejson.values()[0]) == '0' else False
	return is_response_bool
	
	## reset not working yet 03/03/2017 CY
    def reset(self): 
        response = str(self._device.CloseCommunicationAndReinitializeCamera())
        responsejson = json.loads(response)
        is_response_bool = True if str(responsejson.values()[0]) == '0' else False
	return is_response_bool

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
        

    def prep_run_sequence(self):
        response = str(self._device.PrepareForRun()).replace('\r\n', '')
        responsejson = json.loads(response)
        is_response_bool = True if str(responsejson.values()[0]) == '0' else False
        return is_response_bool

		
		
#####################################################################################################
## Image Analysis

#result = mpkapi.PrepareForRun()
#print(String.Format("Prepare For Run - ErrorCode: {0}", result['ErrorCode']))


#####################################################################################################
## Data Logging

    def exportlog(self, imagekey, log_path, filename):
	export_action = self._device.ExportData(imagekey, log_path, filename)
        response = str(export_action).replace('\r\n', '')
        responsejson = json.loads(response)
        is_response_bool = True if str(responsejson.values()[0]) == '0' else False
        return is_response_bool

if __name__ == "__main__":
    verbose=True
    focus_distance=0.50
    lens_aperture=2.8
    auto_exposure=False
    cx = 1816 #Left
    cy = 740 #Top
    cl = 1446 #Width
    cw = 1575 #Height
    rect = Rectangle(cx, cy, cl, cw)
    the_instrument = I16(verbose, focus_distance, lens_aperture, auto_exposure, rect)
    sn = the_instrument.serialnumber()
    isinit = the_instrument.init(sn)

    mpkapi_version = the_instrument.mpkapi_version()
    tt_version = the_instrument.tt_version()
    the_instrument.is_ready()
    ## Define per pattern measurement setups
    eR_GL255 = 156.29
    eG_GL255 = 243.88
    eB_GL255 = 160.00
    the_instrument.measurementsetup("GL255", eR_GL255, eG_GL255, eB_GL255)
    eR_GL180 = 256.29
    eG_GL180 = 343.88
    eB_GL180 = 190.00	
    the_instrument.measurementsetup("GL180",  eR_GL180, eG_GL180, eB_GL180)	
    the_instrument.measurementsetup("GL127", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL090", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL064", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL035", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL025", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL012", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("GL008", 5000, 5000, 5000)
    the_instrument.measurementsetup("GL003", 5000, 5000, 5000)
    the_instrument.measurementsetup("Red", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("Green", 156.29, 243.88, 160.00)
    the_instrument.measurementsetup("Blue", 156.29, 243.88, 160.00)

    the_instrument.getcolorcalibrationlist() #11
    the_instrument.getcolorshiftcalibrationlist() #6
    the_instrument.getimagescalecalibrationlist() #3
    the_instrument.getflatfieldcalibrationlist() #6

    meassetup = "GL255" # Make sure name should be same as pattern/meas_setup string
    colorcalibrationid = 1
    imagescaleid = 0
    colorshiftid = 1
    the_instrument.setcalibrationid(meassetup, colorcalibrationid, imagescaleid, colorshiftid) 

    pattern = "GL255"
    imagekey = "whitekey" # can be set by end user.
    isSavetoDatabase = True
    the_instrument.capture(meassetup, imagekey, isSavetoDatabase)

    the_instrument.close_comm()

    the_instrument.prep_run_sequence()
    log_path = os.path.join(os.getcwd(), 'testlog')
    filename = imagekey
    is_log_success = the_instrument.exportlog(imagekey, log_path, filename)







