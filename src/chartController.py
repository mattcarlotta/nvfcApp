#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.widgets import Button
from matplotlib import animation, style
from dataController import *
from dragHandler import *
from messageController import displayDialogBox, displayErrorBox
try:
	# python3
	from tkinter import filedialog
except ImportError:
	# python2
	import tkFileDialog as filedialog

import sys
from nvFspd import NvidiaFanController, updatedCurve
from os import path
import csv

style.use(['fivethirtyeight']) # current plot theme

""" Global Variables """
fig = plt.figure(num="Nvidia Fan Controller", figsize=(12, 9)) # create a figure (one figure per window)
fig.subplots_adjust(left=0.11, bottom=0.15, right=0.94, top=0.89, wspace=0.2, hspace=0)
axes = fig.add_subplot(1,1,1) # add a subplot to the figure. axes is of type Axes which contains most of the figure elements
update_stats = True # sets flag for updating chart with GPU stats
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # ticks across x and y axes
# default curve values
x_values = [0, 	11, 23, 34, 45, 55, 65, 74, 81, 88, 94, 100]
y_values = [10, 15, 21, 27, 34, 41, 50, 59, 68, 78, 88, 100]
loadedConfigDir = None # stores an opened config file path in case the curve is reset
""" --------------- """

class Chart():
	def __init__(self, notebook):
		global nvidiaController
		global dataController
		global line

		initChartValues()
		self.plot = plt # add plt instance
		self.fig = fig # add plt.figure instance
		self.axes = axes # add a subplot instance to the figure
		self.canvas = FigureCanvas(self.fig) # add fig instance to a figure canvas
		self.canvas.set_size_request(800, 600) # set default canvas height (req'd for displaying the chart)

		# appends the chart => to a box => to a notebook
		self.graphTab = Gtk.Box()
		self.graphTab.add(self.canvas) # add plt figure canvas to the newly created gtkBox
		notebook.append_page(self.graphTab, Gtk.Label('Graph')) # add the gtkBox to the notebook

		# updates chart with GPU stats every 1000ms
		self.anim = animation.FuncAnimation(self.fig, updateLabelStats, interval=1000)

		# chart min/max values for the background grid layout
		self.x_min = -5
		self.x_max = 105
		self.y_min = 0
		self.y_max = 105
		self.axes.set_xlim(self.x_min, self.x_max)
		self.axes.set_xticks(ticks)
		self.axes.set_ylim(self.y_min, self.y_max)
		self.axes.set_yticks(ticks)
		self.axes.tick_params(colors='0.7', which='both', labelsize=12)
		self.axes.grid(linestyle='-', linewidth='0.1', color='grey') # background lines (thin and grey)

		# misc. chart configurations
		self.axes.axhline(y=10, xmin=0, xmax=1, linewidth=1, color='red') # red line across @ (10, 0) to represent lowest value
		self.axes.set_title("GPU Fan Controller", fontsize=16)
		for axis in ['bottom','left']: self.axes.spines[axis].set_color('0.1')
		self.plot.setp(self.axes.spines.values(), linewidth=0.2)
		# self.fig.patch.set_facecolor('0.15') # sets background color

		# matplotlib stops working if two buttons aren't present
		# for ax in [-100,100]: self.fig.add_axes([0, ax, 0.01, 0.01]) # [lft, bttm, w, h]

		# creates curve w/ options: color=blue, s=squares, picker=max distance for selection
		line, = axes.plot(x_values, y_values, linestyle='-',  marker='s', markersize=4.5, color='b', picker=5, linewidth=1.5)

		self.dragHandler = DragHandler(self) # handles the mouse clicks on the curve
		dataController = DataController(x_values, y_values) # handles updating curve data

		# starts updating the GPU fan speeds
		nvidiaController = NvidiaFanController(x_values, y_values)
		nvidiaController.start()

def close():
	plt.close('all')
	nvidiaController.stop()

def applyData():
	xdata = line.get_xdata() # grabs current curve y data
	ydata = line.get_ydata() # grabs current curve y data
	is_valid_curve = dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

	if is_valid_curve:
		updateChart(xdata, ydata) # updates nvFspd.NvidiaFanController() with new curve data
		displayDialogBox('Successfully applied the current curve to the fan settings!')
	else:
		xdata, ydata = dataController.getData() # gets previous data
		line.set_data([xdata, ydata]) # resets line to previous curve

def initChartValues():
	file = loadedConfigDir or "config.csv"
	# loads configuration array [temp, fspd] from csv
	if path.exists(file): setDataFromFile(file)


def openFile():
	global loadedConfigDir

	file = filedialog.askopenfilename(
		title="Select configuration",
		filetypes=[('csv files', ".csv")])

	if not file: return # if dialog is canceled

	xdata, ydata = setDataFromFile(file)

	if xdata and ydata:
		line.set_data([xdata, ydata]) # update curve with values
		updateChart(x_values, y_values) # update chart to reflect values
		loadedConfigDir = file

def resetData():
	initChartValues() # reset to initial values
	line.set_data([x_values, y_values]) # update curve with values
	updateChart(x_values, y_values) # update chart to reflect values

def saveToFile():
	config = '' # initialize config variable
	xdata, ydata = dataController.getData() # get current curve points

	for index in range(0, len(xdata)):
		config += str(xdata[index]) + "," + str(ydata[index]) + "\n" # combines x and y curve data: (x, y) (x, y)

	# default saved as *.csv
	file = filedialog.asksaveasfile(
		title="Save configuration",
		mode='w',
		filetypes=[('csv files', ".csv")],
		defaultextension=".csv")

	if file is None: return # if dialog is canceled

	file.write(str(config)) # write string to file
	file.close() # close instance
	displayDialogBox('Successfully saved the current curve configuration!')

def setDataFromFile(file):
	global x_values
	global y_values

	try:
		cfg_x = []
		cfg_y = []
		with open(file, 'r') as csvfile:
			config = csv.reader(csvfile, delimiter=',')
			for row in config:
				cfg_x.append(int(row[0]))
				cfg_y.append(int(row[1]))

		# updates default curve values with config array
		x_values = cfg_x #temp
		y_values = cfg_y #speed
		return cfg_x, cfg_y
	except:
		displayErrorBox("Failed to load configuration file.")

def setUpdateStats(bool):
	global update_stats
	update_stats = bool # whether or not to update GPU stats

def stopControlling():
	setUpdateStats(False)
	nvidiaController.stop()
	plt.cla()
	axes.set_title("GPU Fan Controller", fontsize=16, color='grey', pad=20)

def stopAndClearChart():
	stopControlling()
	displayErrorBox("There was an error when attempting to read GPU statistics. Please make sure you're using the proprietary Nvidia drivers and that they're currently in use.")

def updateChart(xdata, ydata):
	setUpdateStats(False) # temporarily stops live GPU updates
	updatedCurve(True) # pauses the nvFspd run loop
	nvidiaController.setCurve(xdata, ydata) # updates curve with new x and y data
	updatedCurve(False) # resumes nvFspd loop
	setUpdateStats(True) # enables live GPU updates

def updateLabelStats(i):
	if (update_stats):
		try:
			current_temp = NvidiaFanController().checkGPUTemp() # grabs current temp from NvidiaFanController
			current_fan_speed = NvidiaFanController().checkFanSpeed() # grabs current fspd from NvidiaFanController

			# check to see if values are present
			if not current_temp or current_fan_speed: raise ValueError('')

			# updates chart labels
			axes.set_xlabel("Temperature "+ "(" + str(current_temp) + u"°C)", fontsize=12, labelpad=20)
			axes.set_ylabel("Fan Speed " + "(" + str(current_fan_speed) + u"%)", fontsize=12, labelpad=10)
		except ValueError:
			stopAndClearChart()

"""
def updateLabelStats(i):
	if (update_stats):
		current_temp = NvidiaFanController().checkGPUTemp() # grabs current temp from NvidiaFanController
		current_fan_speed = NvidiaFanController().checkFanSpeed() # grabs current fspd from NvidiaFanController

		if not current_temp or current_fan_speed: return stopAndClearChart()
			# Gtk.main_quit()

		# updates chart labels
		axes.set_xlabel("Temperature "+ "(" + str(current_temp) + u"°C)", fontsize=12, labelpad=20)
		axes.set_ylabel("Fan Speed " + "(" + str(current_fan_speed) + u"%)", fontsize=12, labelpad=10)
"""

if __name__ == '__main__':
	print ('Please launch GUI')
