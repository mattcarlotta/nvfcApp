#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

""" Main application--embed Matplotlib figure in window with UI """

import gi
gi.require_version('Gtk', '3.0')

import numpy as np
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.widgets import Button
from matplotlib import animation, style
from dataController import *
from dragHandler import *
from messageController import displayDialogBox
import sys
import math
# import nvFspd
from nvFspd import NvidiaFanController, updatedCurve
import os
from os import path
import csv


""" Global Variables """
fig = plt.figure(num="Nvidia Fan Controller", figsize=(12, 9)) # create a figure (one figure per window)
axes = fig.add_subplot(111) # add a subplot to the figure. axes is of type Axes which contains most of the figure elements
canvas = FigureCanvas(fig)
canvas.set_size_request(800, 600)
update_stats = True # sets flag for updating chart with GPU stats
x_min = -5
x_max = 105
y_min = 25
y_max = 105
axes.set_title("GPU Fan Controller")
axes.grid()
axes.set_xlim(x_min, x_max)
axes.set_ylim(y_min, y_max)
""" --------------- """


class Chart():
    def __init__(self, chartBox):
        global current_temp
        global current_fan_speed
        global nvidiaController
        global fig
        global dataController
        global line

        initChartValues()
        self.plot = plt
        self.fig = fig
        self.axes = axes
        self.canvas = canvas
        chartBox.add(self.canvas)
        self.anim = animation.FuncAnimation(self.fig, updateLabelStats, interval=1000)
        
        # chart min/max display values
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # matplotlib stops working if two buttons aren't present
        # [left, bottom, width, height]
        self.fig.add_axes([0, -100, 0.01, 0.01])
        self.fig.add_axes([0, 100, 0.01, 0.01])

        line, = axes.plot(x_values, y_values, linestyle='-', marker='o', color='b', picker=5) #b=blue, o=circle, picker=max distance for 

        self.dragHandler = DragHandler(self)
        dataController = DataController(x_values, y_values)

        #validate points from file!
        nvidiaController = NvidiaFanController(x_values, y_values)
        nvidiaController.start()

    def close(self=None, widget=None, *data):
        plt.close('all')
        nvidiaController.stop()
        # Gtk.main_quit()
    
def applyData():
    xdata = line.get_xdata() # grabs current curve y data
    ydata = line.get_ydata() # grabs current curve y data
    is_valid_curve = dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

    if is_valid_curve:
        updateChart(xdata, ydata) # updates nvFspd.NvidiaFanController() with new curve data
        displayDialogBox('Successfully applied the current curve to the fan settings!')
    else:
        xdata, ydata = dataController.getData() # gets previous data
        xydata = [xdata, ydata] 
        line.set_data(xydata) # resets line to previous curve

def initChartValues():
    global x_values
    global y_values

    x_values = [0,  10, 20, 30, 40, 50, 60, 65, 70, 80, 90, 100] # default values
    y_values = [30, 35, 40, 45, 55, 60, 65, 70, 75, 85, 95, 100] # default values

    cfg_x = []
    cfg_y = []

    # Load array [temp, fspd] from csv
    if path.exists("config.csv"):
        with open('config.csv', 'r') as csvfile:
            config = csv.reader(csvfile, delimiter=',')
            for row in config:
                cfg_x.append(int(row[0]))
                cfg_y.append(int(row[1]))

        # updates default curve values with csv array
        x_values = cfg_x #temp
        y_values = cfg_y #speed

def resetData():
    initChartValues() # reset to initial values
    xydata = [x_values, y_values]
    line.set_data(xydata) # update curve with values
    updateChart(x_values, y_values) # update chart to reflect values

def saveToFile():
    config = []
    xdata, ydata = dataController.getData() # get current curve points

    for index in range(0, len(xdata)):
        res = [xdata[index], ydata[index]] # combine x and y data
        config.append(res) # append it to config

    savedConfig = np.array(config) # convert config to numpy array (req'd to convert base10 to int)
    np.savetxt("config.csv", savedConfig.astype(int) , delimiter=",", fmt='%i') # saves array[temp, fspd] to config.csv
    displayDialogBox('Successfully saved the current curve configuration!')

def setUpdateStats(bool):
    global update_stats
    update_stats = bool

def updateChart(xdata, ydata):
    """
    Due to how the NvidiaFanController run loop was structured to constantly update, there was an issue where updating the curve points could take anywhere from 3 to 10+ loop iterations
    By pausing the loop, updates to the curve points occur consistently between 1-3 loop iterations
    As a precaution, updating the chart with GPU temp/fan speed stats have also been paused, although may not be necessary.
    """
    setUpdateStats(False) # temporarily stops live GPU updates
    updatedCurve(True) # pauses the nvFspd run loop
    nvidiaController.setCurve(xdata, ydata) # updates curve with new x and y data
    updatedCurve(False) # resumes nvFspd loop
    setUpdateStats(True) # enables live GPU updates

def updateLabelStats(i):
    if (update_stats):
        current_temp = NvidiaFanController().getTemp() # grabs current temp from NvidiaFanController
        axes.set_xlabel("Temperature "+ "(" + str(current_temp) +"°C)") # updates chart x-axis label
        current_fan_speed = str(NvidiaFanController().getFanSpeed()) # grabs current fspd from NvidiaFanController
        axes.set_ylabel("Fan Speed " + "(" + str(current_fan_speed) + "%)") # updates chart y-axis label


if __name__ == '__main__':
    print ('Use GUI')