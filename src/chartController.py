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
from fanController import FanController
from popupController import ErrorDialogBox, MessageDialogBox

style.use(['fivethirtyeight']) # current plot theme


class Chart():
	def __init__(self, parent):
		self.appWindow = parent.appWindow # an instance of appWindow
		self.disableAppButtons = parent.disable_app_buttons # an instance of disable_all_buttons
		self.plt = plt # instance of plt
		self.chartActions = ChartActionController(self) # an instance of chart actions
		self.x_values, self.y_values = self.chartActions.initChartValues() # intialize x and y curve values

		self.fig = self.plt.figure(num="Fan Controller", figsize=(12, 9), facecolor='white') # add plt.figure instance
		self.fig.subplots_adjust(left=0.11, bottom=0.15, right=0.94, top=0.89, wspace=0.2, hspace=0) # adjusts Chart's window
		self.axes = self.fig.add_subplot(111) # add a subplot instance to the figure
		self.canvas = FigureCanvas(self.fig) # add fig instance to a figure canvas
		self.canvas.set_size_request(800, 700) # set default canvas height (req'd for displaying the chart)

		# appends the figure => to the graphBox => to the notebook
		parent.graph.add(self.canvas)

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
		for axis in ['bottom','left', 'top', 'right']: self.axes.spines[axis].set_color('0.1') # adds spines to x and y axes
		self.plt.setp(self.axes.spines.values(), linewidth=0.2) # sets both spines' line widths

		# creates curve w/ options: color=blue, s=squares, picker=max distance for selection
		self.line, = self.axes.plot(self.x_values, self.y_values, linestyle='-',  marker='s', markersize=4.5, color='b', picker=5, linewidth=1.5)

		# drag handler and curve instances
		self.dragHandler = DragHandler(self, self.appWindow) # handles the mouse clicks on the curve
		self.dataController = DataController(self.appWindow, self.x_values, self.y_values) # handles updating curve data

		# starts a stoppable thread (loop that looks for temp changes and updates accordingly)
		self.fanController = FanController(self.x_values, self.y_values)
		self.fanController.start()

	# closes Chart and stops GPU updating
	def close(self):
		plt.close('all')
		self.fanController.stopUpdates()

	# applies Chart's current curve data
	def handleApplyData(self):
		self.chartActions.applyData(self.dataController, self.fanController, self.line)

	# handles GPU control disabling
	def handleDisableGPUControl(self):
		self.setLabelColor('grey', 'grey') # sets label colors
		self.setAxesLabels(0,0) # 0's GPU stats
		self.chartActions.setUpdateStats() # stops live GPU updates
		self.fanController.pause()
		self.fanController.disableFanControl()
		self.dragHandler.setDragControl() # disables dragging curve points
		MessageDialogBox(self.appWindow, "Disabled GPU fan control.")

	# handles GPU control enabling
	def handleEnableGPUControl(self):
		self.setLabelColor('black', 'blue')
		self.chartActions.setUpdateStats() # enables live GPU updates
		self.fanController.resume()
		self.fanController.resetFanControl()
		self.dragHandler.setDragControl() # allows curve points to be dragged
		MessageDialogBox(self.appWindow, "Enabled GPU fan control.")

	# resets Chart's current curve data
	def handleDataReset(self):
		self.chartActions.resetData(self.dataController, self.fanController, self.line)

	# attempts to open and load a config file
	def handleOpenFile(self):
		self.chartActions.initValuesFromOpenFile(self.fanController, self.dataController, self.line)

	# attempts to save a config file
	def handleSaveToFile(self): FileController.saveToFile(self.appWindow, self.dataController)

	# updates Chart's label colors (enabled / disabled)
	def setLabelColor(self, c1, c2):
		self.axes.title.set_color(c1)
		self.axes.xaxis.label.set_color(c1)
		self.axes.yaxis.label.set_color(c1)
		self.plt.setp(self.line, color=c2)

	# updates Chart's GPU stats axes labels
	def setAxesLabels(self, currtmp, currfspd):
		self.axes.set_xlabel("Temperature "+ "(" + str(currtmp) + u"°C)", fontsize=12, labelpad=20)
		self.axes.set_ylabel("Fan Speed " + "(" + str(currfspd) + u"%)", fontsize=12, labelpad=10)

	def updateLabelStats(self, i):
		if (self.chartActions.getUpdatesState()):
			try:
				curr_temp = FanController.temp # grabs current temp
				curr_fspd = FanController.fanspeed # grabs current fspd
				if not curr_temp or not curr_fspd: raise ValueError('Missing temp and/or fan speed') # see if values are present
				self.setAxesLabels(curr_temp, curr_fspd) # updates chart labels
			except ValueError:
				self.disableAppButtons()
				self.chartActions.stopControllingGPU(self.fanController, self.axes)
				ErrorDialogBox(self.appWindow, "There was an error when attempting to read/set GPU stats. Please make sure that you're using the proprietary Nvidia drivers and that they're currently in use. The current Nvidia driver in use is: {0}.".format(self.fanController.getLoadedDriver()))

if __name__ == '__main__':
	print ('Please launch GUI')
