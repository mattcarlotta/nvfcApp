from popupController import ErrorDialogBox


class DataController(object):
	def __init__(self, appWindow, xdata, ydata):
		self.setDataList(xdata, ydata) # initializes x/y data
		self.appWindow = appWindow

	# returns x and y coords (for resetting or saving curve)
	def getData(self): return list(self.xdata), list(self.ydata)

	# attempts to validate and update the curve, then return true or false if successful
	def setData(self, xdata, ydata): return self.setDataList(xdata, ydata) if self.validate(xdata, ydata) == True else False

	# initializes/updates x and y data lists
	def setDataList(self, xdata, ydata):
		self.xdata = list(xdata)
		self.ydata = list(ydata)
		return True

	# validates the set/updated curve
	def validate(self, xdata, ydata):
		invalid = self.validateData(xdata, ydata) # checks if temp and speed are growing exponentially
		return False if invalid else True # return false if curve is invalid, else return true

	# verifies x,y coords, if invalid, returns true else false
	def validateData(self, xdata, ydata):
		first = [0,10]
		last = [100,100]

		# first point temperature must be min.x
		if xdata[0] != first[0]:
			ErrorDialogBox(self.appWindow, "Invalid curve. The first point's temperature (x-value) must be {0}, instead it was {1}.".format(first[0], xdata[0]))
			return True

		# first point speed must be min.y
		if ydata[0] != first[1]:
			ErrorDialogBox(self.appWindow, "Invalid curve. The first point's speed (y-value) must be {0}, instead it was {1}.".format(first[1], ydata[0]))
			return True

		# last point temperature must be lower than max.x
		if xdata[len(xdata) - 1] > last[0]:
			ErrorDialogBox(self.appWindow,"Invalid curve. The last point's temperature (x-value) must be at most {0}, instead it was {1}.".format(last[0], xdata[len(xdata)-1]))
			return True

		# last point speed must be lower than max.y
		if ydata[len(ydata) - 1] > last[1]:
			ErrorDialogBox(self.appWindow, "Invalid curve. The last point's speed (y-value) must be at most {0}, instead it was {1}.".format(last[1], ydata[len(ydata)-1]))
			return True

		# curve must increasing across x,y planes
		for index in range(1, len(xdata)):
			if xdata[index] <= xdata[index - 1] or ydata[index] <= ydata[index - 1]:
				ErrorDialogBox(self.appWindow, "Invalid curve configuration. The curve must be growing linearly or exponentially.")
				return True
