from popupController import ErrorDialogBox

class Curve():
	def __init__(self, xdata, ydata):
		self.set(xdata, ydata) # (arr[...temp], arr[...fspd])

	# appends individual x and y data pairs into a single array [ [temp0, fspd0], [temp1, fspd1], [temp2, fspd2] ...etc ]
	def convertIntoMatrix(self, x_values, y_values):
		self.curve = list()
		x_temp = list(x_values)
		y_speed = list(y_values)
		for index in range(0, len(x_temp)): self.curve.append([x_temp[index], y_speed[index]])

	# used to calculate fan speed based upon GPU temp
	def evaluate(self, x):
		index = 0
		while(index < len(self.curve) - 1 and x):
			if(self.curve[index][0] <= x and self.curve[index + 1][0] > x):
				point_1 = self.curve[index]
				point_2 = self.curve[index + 1]
				delta_x = point_2[0] - point_1[0]
				delta_y = point_2[1] - point_1[1]

				gradient = float(delta_y)/float(delta_x)

				x_bit = x - point_1[0]
				y_bit = int(float(x_bit) * gradient)
				y = point_1[1] + y_bit
				return y

			index += 1

	# sets curve based on args
	def set(self, *args):
		if len(args) == 1: self.curve = list(args[0]) # 1 arr with temp + speed : ([ ...temp], ...fspd])
		if len(args) == 2: self.convertIntoMatrix(args[0], args[1]) # 2 arrs of temp & speed: ([...temp], [...fspd])

if __name__ == '__main__':
	print ('Please launch GUI')
