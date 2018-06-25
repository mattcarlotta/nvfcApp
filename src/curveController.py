from popupController import ErrorDialogBox


class Data(object):
	def __init__(self, xdata, ydata): self.setData(xdata, ydata)

	# gets x and y coords
	def getData(self): return list(self.xdata), list(self.ydata)

	# sets x and y coords
	def setData(self, xdata, ydata):
		self.xdata = list(xdata)
		self.ydata = list(ydata)

class DataController(object):
	def __init__(self, appWindow, xdata, ydata):
		self.data = Data(xdata, ydata)
		self.appWindow = appWindow

	# returns x and y coords (for resetting or saving curve)
	def getData(self): return list(self.data.getData())

	# attempts to validate and update curve
	def setData(self, xdata, ydata):
		if self.validate(xdata, ydata) == True:
			self.data.setData(xdata, ydata)
			return True
		else:
			return False

	def validate(self, xdata, ydata):
		# checks if temp and speed are greater than [min.x, min.y] and less than [max.x, max.y]
		invalid = validateData(self.appWindow, xdata, ydata)

		if invalid: return False

		return True

def validateData(appWindow, xdata, ydata):
	first = [0,10]
	last = [100,100]

	# First point temperature must be min.x
	if xdata[0] != first[0]:
		ErrorDialogBox(appWindow, "Invalid curve. The first point's temperature (x-value) must be {0}, instead it was {1}.".format(first[0], xdata[0]))
		return True

	# First point speed must be min.y
	if ydata[0] != first[1]:
		ErrorDialogBox(appWindow, "Invalid curve. The first point's speed (y-value) must be {0}, instead it was {1}.".format(first[1], ydata[0]))
		return True

	# Last point temperature must be lower than max.x
	if xdata[len(xdata) - 1] > last[0]:
		ErrorDialogBox(appWindow,"Invalid curve. The last point's temperature (x-value) must be at most {0}, instead it was {1}.".format(last[0], xdata[len(xdata)-1]))
		return True

	# Last point speed must be lower than max.y
	if ydata[len(ydata) - 1] > last[1]:
		ErrorDialogBox(appWindow, "Invalid curve. The last point's speed (y-value) must be at most {0}, instead it was {1}.".format(last[1], ydata[len(ydata)-1]))
		return True

	# curve must increasing across x,y planes
	for index in range(1, len(xdata)):
		if xdata[index] <= xdata[index - 1] or ydata[index] <= ydata[index - 1]:
			ErrorDialogBox(appWindow, "Invalid curve configuration. The curve must be growing linearly or exponentially.")
			return True
