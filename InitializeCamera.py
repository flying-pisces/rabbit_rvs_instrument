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
print(mpkapi.GetTrueTestApiVersionInfo())
init_result = mpkapi.InitializeCamera(str(cam_serial['CameraSerial']), False, True)
print(String.Format("Init Camera Result - ErrorCode: {0}", init_result['ErrorCode']))

init_result_sn = mpkapi.InitializeCamera("158683510", False, True)
print init_result_sn


