from msgController import displayErrorBox


class Data(object):
	def __init__(self, xdata, ydata):
		self.setData(xdata, ydata)

	def getData(self):
		xdata = list(self.xdata)
		ydata = list(self.ydata)
		return xdata, ydata

	def setData(self, xdata, ydata):
		self.xdata = list(xdata)
		self.ydata = list(ydata)

class DataController(object):
	def __init__(self, xdata, ydata):
		self.data = Data(xdata, ydata)

	def getData(self):
		return list(self.data.getData())

	def setData(self, xdata, ydata):
		if self.validate(xdata, ydata) == True:
			self.data.setData(xdata, ydata)
			return True
		else:
			return False

	# checks if temp and speed monotonic are greater than zero and checks speed inside [10, 100], temp inside [0,100] ecc ecc
	def validate(self, xdata, ydata):
		first = [0,10]
		last = [100,100]

		if xdata[0] != first[0]:
			# print "ERROR: First point temperature must be ", first[0]
			displayErrorBox("The first point's temperature must be at least {0}".format(first[0]))
			return False
		if ydata[0] < first[1]:
			# print "ERROR: First point speed lower than ", first[1]
			displayErrorBox("The first point's speed must be at least {0}".format(first[1]))
			return False

		if xdata[len(xdata) - 1] < last[0]:
			# print "ERROR: Last point temperature must be ", last[0]
			displayErrorBox("The last point's temperature must be at least {0}".format(last[0]))
			return False
		if ydata[len(ydata) - 1] != last[1]:
			# print "ERROR: Last point speed must be ", last[1]
			displayErrorBox("The last point's speed must be at least {0}".format(last[1]))
			return False

		for index in range(1, len(xdata)):
			if xdata[index] <= xdata[index - 1] or ydata[index] <= ydata[index - 1]:
				# print "ERROR: Curve not increasing!"
				displayErrorBox("The curve needs to be increasing!")
				return False

		return True
