from tkinter import filedialog
import csv
from popupController import ErrorDialogBox, FileChooserBox, FileSaveBox, MessageDialogBox
from curveController import DataController

class FileController():
	# attempts to open, then read a configuration file
	def openFile(appWindow, dataController):
		cfg_x = []
		cfg_y = []

		FileChooserBox(appWindow)
		file = FileChooserBox.dir

		# if dialog is canceled
		if not file: return False, False, False

		# returns read csv xdata/ydata
		cfg_x, cfg_y = FileController.setDataFromFile(appWindow, file)

		# if x or y data not present
		if not (cfg_x or cfg_y): return False, False, False

		# if x or y data not 12 points
		elif len(cfg_x) != 12 or len(cfg_y) != 12: return False, False, False

		# if x or y data does not pass validation
		elif dataController.validate(cfg_x, cfg_y) == False:
			FileChooserBox.dir = None
			return False, False, False

		else: return cfg_x, cfg_y, file

	# attempts to save a configuration file
	def saveToFile(appWindow, dataController):
		config = '' # initialize config string variable
		xdata, ydata = dataController.getData() # get current curve points

		for index in range(0, len(xdata)):
			config += str(xdata[index]) + "," + str(ydata[index]) + "\n" # combines x and y curve data: [x, y] [x, y]...

		# opens a file dialog to save current config to file, returns a temporary file path string if not canceled
		filename = FileSaveBox(appWindow).getFile()

		if filename is None: return # if dialog is canceled

		file = open(filename, "w+") # open file path
		file.write(config) # write config to file path
		file.close() # close instance
		MessageDialogBox(appWindow, 'Successfully saved the current curve configuration!')

	# attempts to read a configuration file
	def setDataFromFile(appWindow, file):
		try:
			cfg_x = []
			cfg_y = []

			with open(file, 'r') as csvfile:
				config = csv.reader(csvfile, delimiter=',')
				for row in config:
					cfg_x.append(int(row[0]))
					cfg_y.append(int(row[1]))

			# check if arrays contain 12 curve point positions
			if len(cfg_x) != 12 or len(cfg_y) != 12: raise Exception('It does not contain 24 curve points!')

			# check if x or y data doesn't pass validation
			elif DataController(appWindow, cfg_x, cfg_y).validate(cfg_x, cfg_y) == False: raise Exception('It does not meet the curve requirements!')

			# updates default curve values with config array
			return cfg_x, cfg_y
		except Exception as error:
			ErrorDialogBox(appWindow, "Failed to load the configuration file: {0}".format(error))
			FileChooserBox.dir = None
			return False, False
