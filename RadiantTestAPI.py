import os
import clr
clr.AddReference('System.Drawing')
apipath = os.path.join(os.getcwd(), "MPK_API.dll")
clr.AddReference(apipath)
from MPK_API import *
from System.Drawing import *
from System import String

mpkapi = MPK_API()

# creating rectangle for subframe region. unit is CCD pixel. Mainly for 4-up. 0,0,camera_ccd_width, camera_ccd_height will be full frame.
# (start x, start y, x width, y width)
#rect = Rectangle(2150, 1340, 500, 500)
rect = Rectangle(0, 0, 1000, 1000)

# InitializeCamera(cameraSerial as String, showFeedbackUI as Boolean)
cam_serial = mpkapi.GetCameraSerial()
print(String.Format("Camera Serial Number: {0}", cam_serial['CameraSerial']))
init_result = mpkapi.InitializeCamera(str(cam_serial['CameraSerial']), False, True)
print(String.Format("Init Camera Result - ErrorCode: {0}", init_result['ErrorCode']))
## mpkapi need parse out after the initialization

################################################################################
#USER XML SETTINGS - 10/25/2016
#The user xml settings 'UserSettings.xml' will be created where the MPK_API.dll lives. If it exists already,
#it needs to be placed wherever the MPK_API.dll resides.
#This contains the:
#	- Camera Calibration Path (the folder where the camera calibration files lives)
#	- Measurement database path
#	- Sequence file path (either a .seqx for single channel or .mseqx for multi channel)
#	- Multi channel analysis - true or false
#	- Measurement Sequence Mode - needs to be either 'Asynchronous' or 'Synchronous'
#	- Analysis Sequence Mode - needs to be either 'Asynchronous' or 'Synchronous'
###############################################################################

########## INITIAL EXP TIME MEAS SETUP #####################
# CreateMeasurementSetup(patternName as String, redEFilterxposure as Single, greenFilterExposure as Single,
#                       blueFilterExposure as Single, xbFilterExposure as Single, focusDistance as Single,
#                       lenAperture as Single, autoAdjustExposure as Boolean, subframeRegion as Rectangle) 
#photopicmeassetup = mpkapi.CreateMeasurementSetup("Photopic", 0, 100.0, 0, 0, 1.0, 2.8, False, rect)
#print(String.Format("Measurement Setup Result for Photopic - ErrorCode: {0}", result['ErrorCode']))

#redphotopicmeassetup = mpkapi.CreateMeasurementSetup("Red", 100.0, 100.0, 100.0, 100.0, 1.0, 2.8, False, rect)
#print(String.Format("Measurement Setup Result for Red - ErrorCode: {0}", result['ErrorCode']))

#greenmeassetup = mpkapi.CreateMeasurementSetup("Green", 100.0, 100.0, 100.0, 100.0, 1.0, 2.8, False, rect)
#print(String.Format("Measurement Setup Result for Green - ErrorCode: {0}", result['ErrorCode']))

#bluemeassetup = mpkapi.CreateMeasurementSetup("Blue", 100.0, 100.0, 100.0, 100.0, 1.0, 2.8, False, rect)
#print(String.Format("Measurement Setup Result for Blue - ErrorCode: {0}", result['ErrorCode']))

whitemeassetup = mpkapi.CreateMeasurementSetup("White", 455, 190, 199, 322, 0.55, 2.8, False, rect)
print(String.Format("Measurement Setup Result for White - ErrorCode: {0}", whitemeassetup['ErrorCode']))
## for Y29, the white exposure time is always set to 0, adjusted_exposure_time, 0, 0. Coz there is no red/blue/XB filter in Y29.

redphotopicmeassetup = mpkapi.CreateMeasurementSetup("Red", 395, 407, 1361, 2151, 0.55, 2.8, False, rect)
print(String.Format("Measurement Setup Result for Red - ErrorCode: {0}", redphotopicmeassetup['ErrorCode']))

greenmeassetup = mpkapi.CreateMeasurementSetup("Green", 689, 196, 1339, 2109, 0.55, 2.8, False, rect)
print(String.Format("Measurement Setup Result for Green - ErrorCode: {0}", greenmeassetup['ErrorCode']))

bluemeassetup = mpkapi.CreateMeasurementSetup("Blue", 700, 410, 139, 220, 0.55, 2.8, False, rect)
print(String.Format("Measurement Setup Result for Blue - ErrorCode: {0}", bluemeassetup['ErrorCode']))
################################################################################

################################################################################
# GetColorCalibrationList(measurementSetupName as String, colorCalibrationID As Integer, imageScaleID as Integer, colorShiftID as Integer)
# It is necessary to get each calibration's description and ID so that the calibration ID may be set.
colorCals = mpkapi.GetColorCalibrationList()
print('Color Cals:')
print(colorCals)
################################################################################

####
#colorshiftCals = mpkapi.GetColorShiftCalibrationList()
#print(colorshiftCals)

#imagescaleCals = mpkapi.GetImageScaleCalibrationList()
#print(imagescaleCals)

###

################################################################################
# SetCalibration(measurementSetupName As String, colorCalibrationID As Integer, imageScaleID As Integer, colorShiftID As Integer)
'''
setwhitecalibration = mpkapi.SetCalibrations("White", 20, 3, 4)
print('Set Calibrations for White')
print(setwhitecalibration)

setredcalibration = mpkapi.SetCalibrations("Red", 20, 3, 4)
print('Set Calibrations for Red')
print(setredcalibration)

setgreencalibration = mpkapi.SetCalibrations("Green", 20, 3, 4)
print('Set Calibrations for Green')
print(setgreencalibration)

setbluecalibration = mpkapi.SetCalibrations("Blue", 20, 3, 4)
print('Set Calibrations for Blue')
print(setbluecalibration)
'''
################################################################################

################################################################################
#SET SERIAL NUMBERS - 10/25/2016
#Channel Index is 0 based.

#Single Channel Result:
'''
resultSN1 = mpkapi.SetSerialNumber("SN1", 0)
print('Serial 1 Set')
print(resultSN1)
'''

#Multi Channel Result:

resultSN1 = mpkapi.SetSerialNumber("SN1", 0)
print('Serial 1 Set')
print(resultSN1)
'''
resultSN2 = mpkapi.SetSerialNumber("SN2", 1)
print('Serial 2 Set')
print(resultSN2)
resultSN3 = mpkapi.SetSerialNumber("SN3", 2)
print('Serial 3 Set')
print(resultSN3)
resultSN4 = mpkapi.SetSerialNumber("SN4", 3)
print('Serial 4 Set')
print(resultSN4)
'''


getSerialResult1 = mpkapi.ReadSerialNumbers(0)
print(getSerialResult1)
'''
getSerialResult2 = mpkapi.ReadSerialNumbers(1)
print(getSerialResult2)

getSerialResult3 = mpkapi.ReadSerialNumbers(2)
print(getSerialResult3)

getSerialResult4 = mpkapi.ReadSerialNumbers(3)
print(getSerialResult4)
'''
################################################################################

## READY TO TAKE MEASUREMENT


################################################################################
# CaptureMeasurement(measurementSetupName as String, imageKey as String, saveToDatabase as Boolean)
capmeasw = mpkapi.CaptureMeasurement("White", "SN_TIME_W", False)
print(String.Format("Measurement Capture Result for White - Image Key: {0}", capmeasw['Imagekey']))
'''
#capmeasr = mpkapi.CaptureMeasurement("Red", "SN_TIME_R", False)
#print(String.Format("Measurement Capture Result for Red - Image Key: {0}", capmeasr['Imagekey']))

#capmeasg = mpkapi.CaptureMeasurement("Green", "SN_TIME_G", False)
#print(String.Format("Measurement Capture Result for Green - Image Key: {0}", capmeasg['Imagekey']))

#capmeasb = mpkapi.CaptureMeasurement("Blue", "SN_TIME_B", False)
#print(String.Format("Measurement Capture Result for Blue - Image Key: {0}", capmeasb['Imagekey']))
'''
################################################################################

################################################################################
# focus - it is recommended that you create a photopic measurement setup
# for example, in the "photopicmeassetup" above, only the photopic filter is used.
# the inner loop part to receive the focus metric is as follows:

#subframe = Rectangle(0, 0, 4896, 3264)

#whitemeassetup1 = mpkapi.CreateMeasurementSetup("White1", 0, 50, 0, 0, 0.45, 8.0, False, subframe)
#print(String.Format("Measurement Setup Result for White 1 - ErrorCode: {0}", whitemeassetup1['ErrorCode']))

#capfocus1 = mpkapi.CaptureMeasurement("White1", "Focus1", False)
#print(String.Format("Image Key: {0}", capfocus1['Imagekey']))

#focusmetric1 = mpkapi.GetFocusMetric("Focus1", rect)
#print(String.Format("Focus Metric Value 1: {0}", focusmetric1['FocusMetric']))

#whitemeassetup2 = mpkapi.CreateMeasurementSetup("White2", 0, 50, 0, 0, 0.5, 8.0, False, subframe)
#print(String.Format("Measurement Setup Result for White 2 - ErrorCode: {0}", whitemeassetup2['ErrorCode']))

#capfocus2 = mpkapi.CaptureMeasurement("White2", "Focus2", False)
#print(String.Format("Image Key: {0}", capfocus2['Imagekey']))

#focusmetric2 = mpkapi.GetFocusMetric("Focus2", rect)
#print(String.Format("Focus Metric Value 2: {0}", focusmetric2['FocusMetric']))

#whitemeassetup3 = mpkapi.CreateMeasurementSetup("White3", 0, 50, 0, 0, 0.65, 8.0, False, subframe)
#print(String.Format("Measurement Setup Result for White 3 - ErrorCode: {0}", whitemeassetup3['ErrorCode']))

#capfocus3 = mpkapi.CaptureMeasurement("White3", "Focus3", False)
#print(String.Format("Image Key: {0}", capfocus3['Imagekey']))

#focusmetric3 = mpkapi.GetFocusMetric("Focus3", rect)
#print(String.Format("Focus Metric Value 3: {0}", focusmetric3['FocusMetric']))

#########

# default folder to save the data C:\Radiant Vision Systems Data\TrueTest\UserData
#################################################################################

#################################################################################
## ExportData(ImageKey as String)
#exportdata = mpkapi.ExportData("SN_TIME_W", "C:\Radiant Vision Systems Data", "W_Image")
#print(String.Format("Export Data Result for White - ErrorCode: {0}", result['ErrorCode']))
'''
exportdata = mpkapi.ExportData("SN_TIME_R", "C:\\oculus\\Tuzi_Cleanroom_Stations\\CV1TestAndFactory\\TestExec\\\thirdparty\\radiant\\Data")
print(String.Format("Export Data Result for Red - ErrorCode: {0}", result['ErrorCode']))

exportdata = mpkapi.ExportData("SN_TIME_G", "C:\\oculus\\Tuzi_Cleanroom_Stations\\CV1TestAndFactory\\TestExec\\\thirdparty\\radiant\\Data")
print(String.Format("Export Data Result for Green - ErrorCode: {0}", result['ErrorCode']))

exportdata = mpkapi.ExportData("SN_TIME_B", "C:\\oculus\\Tuzi_Cleanroom_Stations\\CV1TestAndFactory\\TestExec\\\thirdparty\\radiant\\Data")
print(String.Format("Export Data Result for Blue - ErrorCode: {0}", result['ErrorCode']))
#################################################################################
'''
#################################################################################
## Execute Analyses

result = mpkapi.PrepareForRun()
print(String.Format("Prepare For Run - ErrorCode: {0}", result['ErrorCode']))

result = mpkapi.RunAnalysisByName("RADA","SN_TIME_W","")
print("Run Analysis By Name (RADA)")
print(result)

result = mpkapi.RunAnalysisByName(
    "MU W255","SN_TIME_W",
    "<Parameters>" +
        "<NbrPOICols>15</NbrPOICols>" +
        "<NbrPOIRows>10</NbrPOIRows>" +
    "</Parameters>")

print("Run Analysis By Name (MU W255)")
print(result)

result = mpkapi.RunAnalysisByName(
    "MU G255","SN_TIME_W",
    "<Parameters>" +
        "<NbrPOICols>8</NbrPOICols>" +
        "<NbrPOIRows>8</NbrPOIRows>" +
    "</Parameters>")

print("Run Analysis By Name (MU G255)")
print(result)

#################################################################################

#################################################################################
## Flush Measurement List
#flushmeasresult = mpkapi.FlushMeasurements()
#print(flushmeasresult)
#################################################################################

#################################################################################
## Flush Measurement Setups
#flushmeassetupresult = mpkapi.FlushMeasurementSetups()
#print(flushmeassetupresult)
################################################################################

raw_input("Press Enter to End.")
