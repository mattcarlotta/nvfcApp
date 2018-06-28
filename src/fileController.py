from tkinter import filedialog
import csv
from popupController import ErrorDialogBox, FileChooserBox, FileSaveBox, MessageDialogBox
from dataController import DataController

class FileController():
	# attempts to open, then read a configuration file
	def openFile(appWindow, dataController):
		FileChooserBox(appWindow) # displays file chooser, sets filename string to FileChooserBox.dir
		file = FileChooserBox.dir # gets current filename dir

		# if dialog is canceled, FileChooserBox.dir will be None
		if not file: return False, False, False

		# returns read csv xdata/ydata
		cfg_x, cfg_y = FileController.setDataFromFile(appWindow, file)

		# if x or y data not present
		if not (cfg_x or cfg_y): return False, False, False

		# if x or y data does not pass validation
		elif dataController.validate(cfg_x, cfg_y) == False:
			FileChooserBox.dir = None
			return False, False, False

		else: return cfg_x, cfg_y, file

	# attempts to save a configuration file
	def saveToFile(appWindow, dataController):
		config = '' # initialize config string variable
		xdata, ydata = dataController.getData() # get current curve points

		# combines x and y curve data: config = [x1, y1] [x2, y2] [x3, y3] ...etc
		for index in range(0, len(xdata)): config += "{0},{1}\n".format(xdata[index],ydata[index])

		filename = FileSaveBox(appWindow).getFile() # opens a save config dialog, returns a temp file path string
		if not filename: return # if dialog is canceled

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

			# check if x or y data doesn't pass validation
			if DataController(appWindow, cfg_x, cfg_y).validate(cfg_x, cfg_y) == False: raise Exception('it does not meet the curve requirements!')

			# updates default curve values with config array
			return cfg_x, cfg_y
		except Exception as error:
			ErrorDialogBox(appWindow, "Failed to load the configuration file, {0}".format(error))
			FileChooserBox.dir = None
			return False, False
