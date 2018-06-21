from os import path
from messageController import displayDialogBox
from nvFspd import updatedCurve
from fileController import openFile, setDataFromFile

"""Global Variables"""
loadedConfigDir = None # stores an opened config file path in case the curve is reset
update_stats = True # sets flag for updating chart with GPU stats
""" --------------- """

# updates or reverts curve from current curve x/y values
def applyData(dataController, nvidiaController, line):
	xdata = line.get_xdata() # grabs current curve y data
	ydata = line.get_ydata() # grabs current curve y data
	is_valid_curve = dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

	if is_valid_curve:
		updateChart(nvidiaController, xdata, ydata) # updates nvFspd.NvidiaFanController() with new curve data
		displayDialogBox('Successfully applied the current curve to the fan settings!')
	else:
		xdata, ydata = dataController.getData() # gets previous data
		line.set_data([xdata, ydata]) # resets line to previous curve

# initializes values based upon global x/y values (will always return good x/y coords)
def initChartValues():
	# pre-configured curve
	x_values = [0, 	11, 23, 34, 45, 55, 65, 74, 81, 88, 94, 100]
	y_values = [10, 15, 21, 27, 34, 41, 50, 59, 68, 78, 88, 100]

	file = loadedConfigDir or "default.csv" # load from default or a previously loaded configuration
	# loads configuration array [temp, fspd] from csv
	if path.exists(file):
		cfg_x, cfg_y = setDataFromFile(file)

		# if setDataFromFile returns [None, None], revert back to global x/y values
		if not cfg_x or not cfg_y: return x_values, y_values
		return cfg_x, cfg_y

	return x_values, y_values

def initValuesFromFile(nvidiaController, line):
	global loadedConfigDir

	# attempt to gather curve config from file
	xdata, ydata, file = openFile()

	# if xdata and ydata are present
	if xdata and ydata:
		line.set_data([xdata, ydata]) # update curve with values
		updateChart(nvidiaController, xdata, ydata) # update chart to reflect values
		loadedConfigDir = file

# returns whether or not to enable live updates
def getUpdateStatus(): return update_stats

# resets curve from initial values
def resetData(nvidiaController, line):
	cfg_x, cfg_y = initChartValues() # reset to initial values
	line.set_data([cfg_x, cfg_y]) # update curve with values
	updateChart(nvidiaController, cfg_x, cfg_y) # update chart to reflect values

# clears and disables chart -- triggered when the nvidia settings haven't been configured correctly
def stopControllingGPU(nvidiaController, axes):
	setUpdateStats(False)
	nvidiaController.stop()
	plt.cla()
	axes.set_title("GPU Fan Controller", fontsize=16, color='grey', pad=20)

# determins whether or not the graph will be updating GPU stats
def setUpdateStats(bool):
	global update_stats
	update_stats = bool

# updates chart curve
def updateChart(nvidiaController, xdata, ydata):
	setUpdateStats(False) # temporarily stops live GPU updates
	updatedCurve(True) # pauses the nvFspd run loop
	nvidiaController.setCurve(xdata, ydata) # updates curve with new x and y data
	updatedCurve(False) # resumes nvFspd loop
	setUpdateStats(True) # enables live GPU updates
