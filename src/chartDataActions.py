from os import path
from fanController import FanController
from fileController import FileController
from popupController import FileChooserBox, MessageDialogBox


class ChartActionController():
	def __init__(self, parent):
		super().__init__()
		self.appWindow = parent.appWindow
		self.plt = parent.plt
		self.updates = True
		self.valid_config = True

	# updates or reverts curve from current curve x/y values
	def applyData(self, dataController, fanController, line):
		xdata = line.get_xdata() # grabs current curve y data
		ydata = line.get_ydata() # grabs current curve y data
		is_valid_curve = dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

		if is_valid_curve:
			self.updateChart(fanController, xdata, ydata) # updates FanController() with new curve data
			MessageDialogBox(self.appWindow, 'Successfully applied the current curve to the fan settings!')
		else:
			xdata, ydata = dataController.getData() # gets previous data
			line.set_data([xdata, ydata]) # resets line to previous curve

	# returns update status (T/F)
	def getUpdatesState(self): return self.updates

	# initializes x/y values values from file or preconfigured (will always return good x/y points)
	def initChartValues(self):
		x_values = [0, 11, 23, 34, 45, 55, 65, 74, 81, 88, 94, 100] # pre-configured temp points
		y_values = [10, 15, 21, 27, 34, 41, 50, 59, 68, 78, 88, 100] # pre-configured speed points

		file = FileChooserBox.dir or "default.csv" if self.valid_config else '' # load from default or a previously loaded configuration
		#  check if configuration.csv file still exists
		if path.exists(file):
			cfg_x, cfg_y = FileController.setDataFromFile(self.appWindow, file) # attempt to load config x,y values
			if not cfg_x or not cfg_y: # if setDataFromFile returns [False, False], revert back to global x/y values
				self.valid_config = False # set default.csv/ loaded *.csv to invalid
				return x_values, y_values # return preconfigured values
			else: return cfg_x, cfg_y # returns data from loaded .csv file

		# no default.csv present, returns default values
		return x_values, y_values

	# attempts to open and load configuration files
	def initValuesFromOpenFile(self, fanController, dataController, line):
		xdata, ydata, file = FileController.openFile(self.appWindow, dataController) # attempt to gather curve config data from file
		if xdata and ydata: # if xdata and ydata are present
			line.set_data([xdata, ydata]) # update curve values
			dataController.setData(xdata, ydata) # store curve values
			self.updateChart(fanController, xdata, ydata) # update chart to reflect values
			self.valid_config = True # config is valid, OK to use for curve resetting
		else:
			self.valid_config = False # config is invalid => set this false to prevent invalid curve resetting

	# resets curve to initial values
	def resetData(self, dataController, fanController, line):
		xdata, ydata = self.initChartValues() # reset to initial values
		line.set_data([xdata, ydata]) # update curve values
		dataController.setData(xdata, ydata) # store curve values
		self.updateChart(fanController, xdata, ydata) # update chart to reflect values

	# clears and disables chart -- triggered when the driver settings haven't been configured correctly
	def stopControllingGPU(self, fanController, axes):
		self.setUpdateStats() # stops GPU stat updates
		fanController.stopUpdates() # stops GPU controlling
		self.plt.cla() # clears chart

		# resets axes labels to appear inactive
		axes.set_title("Fan Controller", fontsize=16, color='grey', pad=20) # main title
		axes.set_xlabel(u"Temperature (0°C)", fontsize=12, labelpad=20) # x-axis title
		axes.set_ylabel(u"Fan Speed (0%)", fontsize=12, labelpad=10) # y-axis title
		axes.xaxis.label.set_color('grey') # x-axis title color
		axes.yaxis.label.set_color('grey') # y-axis title color

	# determines whether or not the graph will be updating GPU stats
	def setUpdateStats(self): self.updates = not self.updates

	# updates chart curve
	def updateChart(self, fanController, xdata, ydata):
		fanController.setCurve(xdata, ydata) # updates curve with new x and y data

if __name__ == '__main__':
	print ('Please launch GUI')
