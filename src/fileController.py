try:
	# python3
	from tkinter import filedialog
except ImportError:
	# python2
	import tkFileDialog as filedialog
import csv
from messageController import displayDialogBox, displayErrorBox

def openFile():
	cfg_x = []
	cfg_y = []

	file = filedialog.askopenfilename(
		title="Select configuration",
		filetypes=[('csv files', ".csv")])

	if not file: return False, False, False # if dialog is canceled

	cfg_x, cfg_y = setDataFromFile(file) # returns read csv xdata/ydata

	if not (cfg_x or cfg_y): return False, False, False
	elif len(cfg_x) != 12 or len(cfg_y) != 12: return False, False, False
	else: return cfg_x, cfg_y, file

def saveToFile(dataController):
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
		return False, False
