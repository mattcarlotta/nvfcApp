from chartController import Chart
from chartDataActions import ChartActionController
from dragController import DragHandler
from fanController import NvidiaFanController
from msgController import displayDialogBox

class GPUController():
	# triggered by "Disable" button
	def disableGPUControl():
		Chart.setLabelColor('grey', 'grey') # sets label colors
		Chart.setAxesLabels(0,0) # 0's GPU stats
		ChartActionController.setUpdateStats(False) # stops live GPU updates
		NvidiaFanController.pauseUpdates(True) # temporarily pauses the run loop
		NvidiaFanController.disableFanControl() # resets fan back to auto
		DragHandler.setCurveControl(False) # disables curve points
		displayDialogBox("Disabled GPU fan control.")

	# triggered by "Enable" button
	def enableGPUControl():
		Chart.setLabelColor('black', 'blue')
		ChartActionController.setUpdateStats(True) # enables live GPU updates
		NvidiaFanController.pauseUpdates(False) # unpauses the run loop
		NvidiaFanController.resetFanControl() # resets old_fan_speed to trigger a curve update
		DragHandler.setCurveControl(True) # allows curve points to be moved
		displayDialogBox("Enabled GPU fan control.")
