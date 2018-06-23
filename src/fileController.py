from tkinter import filedialog
import csv
from popupController import ErrorDialogBox, FileChooserBox, FileSaveBox, MessageDialogBox


class FileController():
	# attempts to open, then read a configuration file
	def openFile(parent):
		cfg_x = []
		cfg_y = []

		FileChooserBox(parent)
		file = FileChooserBox.dir

		if not file: return False, False, False # if dialog is canceled

		cfg_x, cfg_y = FileController.setDataFromFile(parent, file) # returns read csv xdata/ydata

		if not (cfg_x or cfg_y): return False, False, False
		elif len(cfg_x) != 12 or len(cfg_y) != 12: return False, False, False
		else: return cfg_x, cfg_y, file

	# attempts to save a configuration file
	def saveToFile(parent, dataController):
		config = '' # initialize config variable
		xdata, ydata = dataController.getData() # get current curve points

		for index in range(0, len(xdata)):
			config += str(xdata[index]) + "," + str(ydata[index]) + "\n" # combines x and y curve data: (x, y) (x, y)

		# attempts to save current config to file, returns file path string if not canceled
		filename = FileSaveBox(parent).getFile()

		if filename is None: return # if dialog is canceled

		file = open(filename, "w+") # open file path
		file.write(config) # write config to file path
		file.close() # close instance
		MessageDialogBox(parent, 'Successfully saved the current curve configuration!')

	# attempts to read a configuration file
	def setDataFromFile(parent, file):
		try:
			cfg_x = []
			cfg_y = []

			with open(file, 'r') as csvfile:
				config = csv.reader(csvfile, delimiter=',')
				for row in config:
					cfg_x.append(int(row[0]))
					cfg_y.append(int(row[1]))

			# check if arrays contain 12 curve point positions
			if len(cfg_x) != 12 or len(cfg_y) != 12: raise Exception('Invalid config')

			# updates default curve values with config array
			return cfg_x, cfg_y
		except Exception as error:
			ErrorDialogBox(parent, "Failed to load configuration file.")
			FileChooserBox.dir = None
			return False, False
