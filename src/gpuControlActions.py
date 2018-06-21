import matplotlib.pyplot as plt
import chartController
import chartDataActions
import dragController
import nvFspd
from messageController import displayDialogBox


# triggered by "Disable" button
def disableGPUControl():
	chartController.setLabelColor('grey', 'grey') # sets label colors
	chartController.setAxesLabels(0,0) # 0's GPU stats
	chartDataActions.setUpdateStats(False) # stops live GPU updates
	nvFspd.updatedCurve(True) # temporarily pauses the nvFspd run loop
	nvFspd.disableFanControl() # resets fan back to auto
	dragController.setCurveControl(False) # disables curve points
	displayDialogBox("Disabled GPU curve fan control. Reverted back to driver control.")

# triggered by "Enable" button
def enableGPUControl():
	chartController.setLabelColor('black', 'blue')
	chartDataActions.setUpdateStats(True) # enables live GPU updates
	nvFspd.updatedCurve(False) # unpauses the nvFspd run loop
	nvFspd.enableFanControl() # resets old_fan_speed to trigger a curve update
	dragController.setCurveControl(True) # allows curve points to be moved
	displayDialogBox("Enabled GPU fan control.")
