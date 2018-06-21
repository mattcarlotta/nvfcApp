#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.widgets import Button
from matplotlib import animation, style
from os import path
import sys

try:
	# python3
	from tkinter import filedialog
except ImportError:
	# python2
	import tkFileDialog as filedialog

try:
	# python3
	from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
except:
	# python2
	from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

import chartDataActions
import curveController
import dragController
from messageController import displayDialogBox, displayErrorBox
import fileController
import nvFspd

style.use(['fivethirtyeight']) # current plot theme

""" Global Variables """
fig = plt.figure(num="Nvidia Fan Controller", figsize=(12, 9)) # create a figure (one figure per window)
fig.subplots_adjust(left=0.11, bottom=0.15, right=0.94, top=0.89, wspace=0.2, hspace=0) # adjusts Chart's window
axes = fig.add_subplot(1,1,1) # add a subplot to the figure
""" --------------- """


class Chart():
	def __init__(self, notebook):
		global nvidiaController
		global dataController
		global line

		self.x_values, self.y_values = chartDataActions.initChartValues() # intialize x and y curve values

		self.plot = plt # add plt instance
		self.fig = fig # add plt.figure instance
		self.axes = axes # add a subplot instance to the figure
		self.canvas = FigureCanvas(self.fig) # add fig instance to a figure canvas
		self.canvas.set_size_request(800, 600) # set default canvas height (req'd for displaying the chart)

		# appends the chart => to a box => to a notebook
		self.graphTab = Gtk.Box() # create box instance
		self.graphTab.add(self.canvas) # add plt figure canvas to the newly created gtkBox
		notebook.append_page(self.graphTab, Gtk.Label('Graph')) # add the gtkBox to the notebook

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
		self.axes.set_title("GPU Fan Controller", fontsize=16) # Chart's title
		for axis in ['bottom','left']: self.axes.spines[axis].set_color('0.1') # adds spines to x and y axes
		self.plot.setp(self.axes.spines.values(), linewidth=0.2) # sets both spines' line widths
		# self.fig.patch.set_facecolor('0.15') # sets background color

		# creates curve w/ options: color=blue, s=squares, picker=max distance for selection
		line, = axes.plot(self.x_values, self.y_values, linestyle='-',  marker='s', markersize=4.5, color='b', picker=5, linewidth=1.5)

		# drag handler and curve instances
		self.dragHandler = dragController.DragHandler(self) # handles the mouse clicks on the curve
		dataController = curveController.DataController(self.x_values, self.y_values) # handles updating curve data

		# starts a stoppable thread (loop that looks for temp changes and updates accordingly)
		nvidiaController = nvFspd.NvidiaFanController(self.x_values, self.y_values)
		nvidiaController.start()

	def updateLabelStats(self, i):
		update_stats = chartDataActions.getUpdateStatus()
		if (update_stats):
			try:
				current_temp = nvFspd.NvidiaFanController().checkGPUTemp() # grabs current temp
				current_fan_speed = nvFspd.NvidiaFanController().checkFanSpeed() # grabs current fspd

				# check to see if values are present
				if not current_temp or not current_fan_speed: raise ValueError('Missing temp and/or fan speed')

				# updates chart labels
				setAxesLabels(current_temp, current_fan_speed)
			except ValueError:
				chartDataActions.stopControllingGPU(nvidiaController, axes)
				displayErrorBox("There was an error when attempting to read GPU statistics. Please make sure you're using the proprietary Nvidia drivers and that they're currently in use.")

# closes Chart and stops GPU updating
def close():
	plt.close('all')
	nvidiaController.stop()

# applies Chart's current curve data
def clickedApplyData():
	chartDataActions.applyData(dataController, nvidiaController, line)

# resets Chart's current curve data
def clickedDataReset():
	chartDataActions.resetData(nvidiaController, line)

# attempts to open and load a config file
def clickedOpenFile():
	chartDataActions.initValuesFromOpenFile(nvidiaController, line)

# attempts to save a config file
def clickedSaveToFile():
	fileController.saveToFile(dataController)

# updates Chart's label colors (enabled / disabled)
def setLabelColor(c1,c2):
	axes.title.set_color(c1)
	axes.xaxis.label.set_color(c1)
	axes.yaxis.label.set_color(c1)
	plt.setp(line, color=c2)

# updates Chart's GPU stats axes labels
def setAxesLabels(currtmp,currfspd):
	axes.set_xlabel("Temperature "+ "(" + str(currtmp) + u"°C)", fontsize=12, labelpad=20)
	axes.set_ylabel("Fan Speed " + "(" + str(currfspd) + u"%)", fontsize=12, labelpad=10)

if __name__ == '__main__':
	print ('Please launch GUI')
