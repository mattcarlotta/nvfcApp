import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib import animation, style
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from subprocess import check_output
from chartDataActions import ChartActionController
from dataController import DataController
from dragController import DragHandler
from fileController import FileController
from fanController import NvidiaFanController
from popupController import ErrorDialogBox


style.use(['fivethirtyeight']) # current plot theme

class Chart():
	""" Class Variables """
	fig = plt.figure(num="Fan Controller", figsize=(12, 9)) # create a figure (one figure per window)
	fig.subplots_adjust(left=0.11, bottom=0.15, right=0.94, top=0.89, wspace=0.2, hspace=0) # adjusts Chart's window
	axes = fig.add_subplot(1,1,1) # add a subplot to the figure
	""" --------------- """

	def __init__(self, appWindow, graphBox, disableAppButtons):
		global nvidiaController
		global dataController
		global line

		self.appWindow = appWindow # an instance of appWindow
		self.disableAppButtons = disableAppButtons # an instand of disable_all_buttons

		self.x_values, self.y_values = ChartActionController.initChartValues(self.appWindow) # intialize x and y curve values

		self.plot = plt # add plt instance
		self.fig = Chart.fig # add plt.figure instance
		self.axes = Chart.axes # add a subplot instance to the figure
		self.canvas = FigureCanvas(self.fig) # add fig instance to a figure canvas
		self.canvas.set_size_request(800, 600) # set default canvas height (req'd for displaying the chart)

		# appends the figure => to the graphBox => to the notebook
		graphBox.add(self.canvas)

		# updates chart with GPU stats every 1000ms
		self.anim = animation.FuncAnimation(self.fig, self.updateLabelStats, interval=1000)

		# chart min/max values for the background grid layout
		self.x_min = -5
		self.x_max = 105
		self.y_min = 0
		self.y_max = 105
		self.ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
		self.axes.set_xlim(self.x_min, self.x_max) # x-axis min/max values
		self.axes.set_ylim(self.y_min, self.y_max) # y-axis min/max values
		self.axes.set_xticks(self.ticks) # x-axis ticks
		self.axes.set_yticks(self.ticks) # y-axis ticks
		self.axes.tick_params(colors='0.7', which='both', labelsize=12)
		self.axes.grid(linestyle='-', linewidth='0.1', color='grey') # background lines (thin and grey)

		# misc. chart configurations
		self.axes.axhline(y=10, xmin=0, xmax=1, linewidth=1, color='red') # red line to represent lowest value (10,0)
		self.axes.set_title("Fan Controller", fontsize=16) # Chart's title
		for axis in ['bottom','left']: self.axes.spines[axis].set_color('0.1') # adds spines to x and y axes
		self.plot.setp(self.axes.spines.values(), linewidth=0.2) # sets both spines' line widths
		# self.fig.patch.set_facecolor('0.15') # sets background color

		# creates curve w/ options: color=blue, s=squares, picker=max distance for selection
		line, = Chart.axes.plot(self.x_values, self.y_values, linestyle='-',  marker='s', markersize=4.5, color='b', picker=5, linewidth=1.5)

		# drag handler and curve instances
		self.dragHandler = DragHandler(self, self.appWindow) # handles the mouse clicks on the curve
		dataController = DataController(self.appWindow, self.x_values, self.y_values) # handles updating curve data

		# starts a stoppable thread (loop that looks for temp changes and updates accordingly)
		nvidiaController = NvidiaFanController(self.x_values, self.y_values)
		nvidiaController.start()

	# closes Chart and stops GPU updating
	def close():
		plt.close('all')
		nvidiaController.stop()

	# applies Chart's current curve data
	def handleApplyData(appWindow): ChartActionController.applyData(appWindow, dataController, nvidiaController, line)

	# resets Chart's current curve data
	def handleDataReset(appWindow): ChartActionController.resetData(appWindow, dataController, nvidiaController, line)

	# attempts to open and load a config file
	def handleOpenFile(appWindow): ChartActionController.initValuesFromOpenFile(appWindow, nvidiaController, dataController, line)

	# attempts to save a config file
	def handleSaveToFile(appWindow): FileController.saveToFile(appWindow, dataController)

	# updates Chart's label colors (enabled / disabled)
	def setLabelColor(c1,c2):
		Chart.axes.title.set_color(c1)
		Chart.axes.xaxis.label.set_color(c1)
		Chart.axes.yaxis.label.set_color(c1)
		plt.setp(line, color=c2)

	# updates Chart's GPU stats axes labels
	def setAxesLabels(currtmp, currfspd):
		Chart.axes.set_xlabel("Temperature "+ "(" + str(currtmp) + u"°C)", fontsize=12, labelpad=20)
		Chart.axes.set_ylabel("Fan Speed " + "(" + str(currfspd) + u"%)", fontsize=12, labelpad=10)

	def updateLabelStats(self, i):
		update_stats = ChartActionController.update_stats
		if (update_stats):
			try:
				curr_temp = NvidiaFanController.temp # grabs current temp
				curr_fspd = NvidiaFanController.fanspeed # grabs current fspd

				# check to see if values are present
				if not curr_temp or not curr_fspd: raise ValueError('Missing temp and/or fan speed')

				# updates chart labels
				Chart.setAxesLabels(curr_temp, curr_fspd)
			except ValueError:
				self.disableAppButtons()
				ChartActionController.stopControllingGPU(nvidiaController, Chart.axes)
				driver_version = NvidiaFanController.drv_ver
				ErrorDialogBox(self.appWindow, "There was an error when attempting to read/set GPU statistics. Please make sure that you're using the proprietary Nvidia drivers and that they're currently in use. The current Nvidia driver in use is: {0}.".format(driver_version))

if __name__ == '__main__':
	print ('Please launch GUI')
