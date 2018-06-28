import matplotlib.pyplot as plt
from os import path
from fanController import FanController
from fileController import FileController
from popupController import FileChooserBox, MessageDialogBox

class ChartActionController():
	""" Class Variables """
	update_stats = True # sets flag for updating chart with GPU stats
	valid_config = True # valid config file
	""" --------------- """

	# updates or reverts curve from current curve x/y values
	def applyData(appWindow, dataController, fanController, line):
		xdata = line.get_xdata() # grabs current curve y data
		ydata = line.get_ydata() # grabs current curve y data
		is_valid_curve = dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

		if is_valid_curve:
			ChartActionController.updateChart(fanController, xdata, ydata) # updates FanController() with new curve data
			MessageDialogBox(appWindow, 'Successfully applied the current curve to the fan settings!')
		else:
			xdata, ydata = dataController.getData() # gets previous data
			line.set_data([xdata, ydata]) # resets line to previous curve

	# initializes values based upon global x/y values (will always return good x/y coords)
	def initChartValues(appWindow):
		# pre-configured curve
		x_values = [0, 	11, 23, 34, 45, 55, 65, 74, 81, 88, 94, 100]
		y_values = [10, 15, 21, 27, 34, 41, 50, 59, 68, 78, 88, 100]

		# if ChartActionController.valid_config:
		file = FileChooserBox.dir or "default.csv" if ChartActionController.valid_config else ''# load from default or a previously loaded configuration

		# loads configuration array [temp, fspd] from csv
		if path.exists(file):
			cfg_x, cfg_y = FileController.setDataFromFile(appWindow, file)

			# if setDataFromFile returns [False, False], revert back to global x/y values
			if not cfg_x or not cfg_y: return x_values, y_values

			# returns data from loaded file
			return cfg_x, cfg_y

		# returns default values
		return x_values, y_values

	# attempts to open and load configuration files
	def initValuesFromOpenFile(appWindow, fanController, dataController, line):
		xdata, ydata, file = FileController.openFile(appWindow, dataController) # attempt to gather curve config data from file

		# if xdata and ydata are present
		if xdata and ydata:
			line.set_data([xdata, ydata]) # update curve values
			dataController.setData(xdata, ydata) # store curve values
			ChartActionController.updateChart(fanController, xdata, ydata) # update chart to reflect values
			ChartActionController.setValidConfig(True)
		else:
			ChartActionController.setValidConfig(False) # config is invalid set this false to prevent invalid curve resetting

	# resets curve to initial values
	def resetData(appWindow, dataController, fanController, line):
		xdata, ydata = ChartActionController.initChartValues(appWindow) # reset to initial values
		line.set_data([xdata, ydata]) # update curve values
		dataController.setData(xdata, ydata) # store curve values
		ChartActionController.updateChart(fanController, xdata, ydata) # update chart to reflect values

	def setValidConfig(bool): ChartActionController.valid_config = bool

	# clears and disables chart -- triggered when the nvidia settings haven't been configured correctly
	def stopControllingGPU(fanController, axes):
		ChartActionController.setUpdateStats() # stops GPU stat updates
		fanController.stopUpdates() # stops GPU controlling
		plt.cla() # clears chart

		# resets axes labels to appear inactive
		axes.set_title("Fan Controller", fontsize=16, color='grey', pad=20)
		axes.set_xlabel(u"Temperature (0°C)", fontsize=12, labelpad=20)
		axes.set_ylabel(u"Fan Speed (0%)", fontsize=12, labelpad=10)
		axes.xaxis.label.set_color('grey')
		axes.yaxis.label.set_color('grey')

	# determines whether or not the graph will be updating GPU stats
	def setUpdateStats(): ChartActionController.update_stats = not ChartActionController.update_stats

	# updates chart curve
	def updateChart(fanController, xdata, ydata):
		fanController.setCurve(xdata, ydata) # updates curve with new x and y data
