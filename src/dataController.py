from popupController import ErrorDialogBox

# handles curve x,y data coordinates
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
		# checks if curve has been supplied 24 points
		if len(xdata) != 12 or len(ydata) != 12:
			ErrorDialogBox(self.appWindow, "Invalid curve. The curve must have 12 temperature and 12 fan speed points. Instead, received: {0}.".format(len(xdata) + len(ydata)))
			return True

		# first and last point's [temp,fspd] must be: [0, 10] and [100, 100]
		for args in [
			[ xdata[0], 0, 'temperature (x-value)', 'first'], # temp [x, 10] = 0
			[ ydata[0], 10, 'speed (y-value)', 'first' ], # fspd [0, x] = 10
			[ xdata[len(xdata) - 1], 100, 'temperature (x-value)', 'last' ], # temp [x, 100] = 100
			[ ydata[len(ydata) - 1], 100, 'speed (y-value)', 'last' ] # fspd [100, x] = 100
		]:
			if args[0] != args[1]:
				ErrorDialogBox(self.appWindow, "Invalid curve. The {0} point's {1} must be {2}, instead it was {3}.".format(args[3], args[2], args[1], args[0]))
				return True

		# curve must increasing across x,y planes
		for index in range(1, len(xdata)):
			if xdata[index] <= xdata[index - 1] or ydata[index] <= ydata[index - 1]:
				ErrorDialogBox(self.appWindow, "Invalid curve configuration. The curve must be growing linearly or exponentially.")
				return True
