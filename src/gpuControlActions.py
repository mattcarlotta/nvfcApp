import matplotlib.pyplot as plt
from chartController import setLabelColor, setAxesLabels
from chartDataActions import setUpdateStats
from dragHandler import setCurveControl
from nvFspd import enableFanControl, disableFanControl, updatedCurve
from messageController import displayDialogBox

# triggered by "Disable" button
def disableGPUControl():
	setLabelColor('grey', 'grey') # sets label colors
	setAxesLabels(0,0) # 0's GPU stats
	setUpdateStats(False) # stops live GPU updates
	updatedCurve(True) # temporarily pauses the nvFspd run loop
	disableFanControl() # resets fan back to auto
	setCurveControl(False) # disables curve points
	displayDialogBox("Disabled GPU curve fan control. Reverted back to driver control.")

# triggered by "Enable" button
def enableGPUControl():
	setLabelColor('black', 'blue')
	setUpdateStats(True) # enables live GPU updates
	updatedCurve(False) # unpauses the nvFspd run loop
	enableFanControl() # resets old_fan_speed to trigger a curve update
	setCurveControl(True) # allows curve points to be moved
	displayDialogBox("Enabled GPU fan control.")
