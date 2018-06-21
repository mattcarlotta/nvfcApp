try:
	# python3
	from tkinter import filedialog
except ImportError:
	# python2
	import tkFileDialog as filedialog
import csv
from messageController import displayDialogBox, displayErrorBox

"""Global Variables"""
loadedConfigDir = None # stores an opened config file path in case the curve is reset
""" --------------- """

def getLoadedConfigDir(): return loadedConfigDir

def openFile():
	global loadedConfigDir

	file = filedialog.askopenfilename(
		title="Select configuration",
		filetypes=[('csv files', ".csv")])

	if not file: return # if dialog is canceled

	xdata, ydata = setDataFromFile(file) # returns read csv xdata/ydata

	if xdata and ydata:
		line.set_data([xdata, ydata]) # update curve with values
		updateChart(x_values, y_values) # update chart to reflect values
		loadedConfigDir = file

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

	file.write(config) # write config string to file
	file.close() # close instance
	displayDialogBox('Successfully saved the current curve configuration!')

def setDataFromFile(file):
	try:
		cfg_x = []
		cfg_y = []
		with open(file, 'r') as csvfile:
			config = csv.reader(csvfile, delimiter=',')
			for row in config:
				cfg_x.append(int(row[0]))
				cfg_y.append(int(row[1]))

		# check if arrays contain 12 curve positions
		if len(cfg_x) != 12 or len(cfg_y) != 12: raise Exception('Invalid config')

		# updates default curve values with config array
		return cfg_x, cfg_y
	except Exception as error:
		displayErrorBox("Failed to load configuration file.")
		return None, None
