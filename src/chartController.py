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
import nvFspd
import os
from os import path
import csv

x_values = []
y_values = []
update_stats = True # sets flag for updating chart with GPU stats
updatedCurve = nvFspd.updatedCurve


class Chart():
    def __init__(self, chartBox):
        global current_temp
        global current_fan_speed
        global nvidiaController

        initChartValues()
        self.plot = plt
        self.fig = plt.figure(num="Nvidia Fan Controller", figsize=(12, 9)) # create a figure (one figure per window)
        self.axes = self.fig.add_subplot(111) # add a subplot to the figure. axes is of type Axes which contains most of the figure elements
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(800, 600)
        chartBox.add(self.canvas)
        self.anim = animation.FuncAnimation(self.fig, self.updateLabelStats, interval=1000)
        

        # working on the Axes object
        self.axes.set_title("GPU Fan Controller") # title for the chart
        self.axes.grid()

        # chart min/max display values
        self.x_min = -5
        self.x_max = 105
        self.y_min = 25
        self.y_max = 105
        self.axes.set_xlim(self.x_min, self.x_max)
        self.axes.set_ylim(self.y_min, self.y_max)

        # Save button
        saveFig = self.fig.add_axes([0.8, 0.015, 0.1, 0.04])
        self.saveFig = Button(saveFig, "Save")
        self.saveFig.on_clicked(self.saveToFile)

        # printAxes = self.fig.add_axes([0.2, 0.025, 0.1, 0.04])  #position rect [left, bottom, width, height] where all quantities are in fractions of figure width and height
        # self.printButton = Button(printAxes, "Print")
        # self.printButton.on_clicked(self.printData)

        # Reset button
        resetChart = self.fig.add_axes([0.125, 0.015, 0.1, 0.04])
        self.resetChart = Button(resetChart, "Reset")
        self.resetChart.on_clicked(self.resetData)

        # Apply button
        applyAxes = self.fig.add_axes([0.685, 0.015, 0.1, 0.04])
        self.applyAxes = Button(applyAxes, "Apply")
        self.applyAxes.on_clicked(self.applyData)

        #b=blue, o=circle, picker=max distance for considering point as clicked
        self.line, = self.axes.plot(x_values, y_values, linestyle='-', marker='o', color='b', picker=5) #tuple unpacking: this function returns a tuple, with the comma we take the first element

        self.dragHandler = DragHandler(self)
        self.dataController = DataController(x_values, y_values)

        #validate points from file!
        # self.updatedCurve = nvFspd.updatedCurve
        # self.nvidiaController = nvFspd.NvidiaFanController(x_values, y_values)
        nvidiaController = nvFspd.NvidiaFanController(x_values, y_values)
        nvidiaController.start()

        # self.fig.canvas.mpl_connect("close_event", self.on_close)
        # self.draw_plot()

    def exit_signal_handler(self, signal, frame):
        plt.close('all')
        nvidiaController.stop()
        # Gtk.main_quit()

    def close(self=None, widget=None, *data):
        plt.close('all')
        nvidiaController.stop()
        # Gtk.main_quit()

    def resetData(self, event):
        initChartValues() # reset to initial values
        xydata = [x_values, y_values]
        self.line.set_data(xydata) # update curve with values
        self.updateChart(x_values, y_values) # update chart to reflect values

    def updateChart(self, xdata, ydata):
        """
        Due to how the NvidiaFanController run loop was structured to constantly update, there was an issue where updating the curve points could take anywhere from 3 to 10+ loop iterations
        By pausing the loop, updates to the curve points occur consistently between 1-3 loop iterations
        As a precaution, updating the chart with GPU temp/fan speed stats have also been paused, although may not be necessary.
        """
        self.setUpdateStats(False) # temporarily stops live GPU updates
        updatedCurve(True) # pauses the nvFspd run loop
        nvidiaController.setCurve(xdata, ydata) # updates curve with new x and y data
        updatedCurve(False) # resumes nvFspd loop
        self.setUpdateStats(True) # enables live GPU updates

    def setUpdateStats(self, bool):
        global update_stats
        update_stats = bool

    def applyData(self, event):
        xdata = self.line.get_xdata() # grabs current curve y data
        ydata = self.line.get_ydata() # grabs current curve y data
        is_valid_curve = self.dataController.setData(xdata, ydata) # checks if curve is exponentially growing (returns bool)

        if is_valid_curve:
            self.updateChart(xdata, ydata) # updates nvFspd.NvidiaFanController() with new curve data
            displayDialogBox('Successfully applied the current curve to the fan settings!')
        else:
            xdata, ydata = self.dataController.getData() # gets previous data
            xydata = [xdata, ydata] 
            self.line.set_data(xydata) # resets line to previous curve

    def saveToFile(self, event):
        config = []
        xdata, ydata = self.dataController.getData() # get current curve points

        for index in range(0, len(xdata)):
            res = [xdata[index], ydata[index]] # combine x and y data
            config.append(res) # append it to config

        savedConfig = np.array(config) # convert config to numpy array (req'd to convert base10 to int)
        np.savetxt("config.csv", savedConfig.astype(int) , delimiter=",", fmt='%i') # saves array[temp, fspd] to config.csv
        displayDialogBox('Successfully saved the current curve configuration!')
    
    def updateLabelStats(self, i):
        if (update_stats):
            current_temp = nvFspd.NvidiaFanController().getTemp() # grabs current temp from NvidiaFanController
            self.axes.set_xlabel("Temperature "+ "(" + str(current_temp) +"°C)") # updates chart x-axis label
            current_fan_speed = str(nvFspd.NvidiaFanController().getFanSpeed()) # grabs current fspd from NvidiaFanController
            self.axes.set_ylabel("Fan Speed " + "(" + str(current_fan_speed) + "%)") # updates chart y-axis label

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

if __name__ == '__main__':
    print ('Use GUI')