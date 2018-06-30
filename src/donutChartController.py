import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class DonutChart():
	def __init__(self, *args):
		self.box = args[0] # gtkBox from builder
		self.radius, self.width = args[1] # donut radius and width
		self.getStat = args[2] # function that returns stat
		self.supTitle = args[3] # supertitle's title
		self.supXPos, self.supYPos = args[4] # supertitle x and y pos
		self.stat = self.getStat() # grabs current stat number
		self.old_stat = 0 # initialize a compare variable to avoid unnecessary redraws
		self.maxStat = args[5] # max range of donut
		self.statType = args[6] # type of stat (%, Mib, MHz, W)
		self.statFontSize, self.supFontSize = args[7] # stat and supertitle font sizes
		self.cnvsHeight, self.cnvsWidth = args[8] # canvas width and height
		self.a = plt.cm.Blues # fill color
		self.b = plt.cm.Greys # negative color
		self.fig, self.ax = plt.subplots(1) # sets a single subsplot
		self.fig.patch.set_facecolor('white') # sets background to white
		self.createDonut() # creates donut chart
		self.createAxis() # creates equal borders and sets title
		self.canvas = FigureCanvas(self.fig) # attach fig to a canvas
		self.canvas.set_size_request(self.cnvsHeight, self.cnvsWidth) # sets canvas size
		self.box.add(self.canvas) # adds canvas to specified gtkBox
		self.anim = animation.FuncAnimation(self.fig, self.update, interval=1000, blit=True) # runs animation to update stats

	def createDonut(self):
		self.donut, _ = self.ax.pie([self.stat, self.maxStat-self.stat], radius=self.radius, colors=[self.a(0.6), self.b(0.6)], counterclock=False, startangle=180)
		plt.setp(self.donut, width=0.2, edgecolor='white') # sets the circle width and adds a white border color

	def createAxis(self):
		self.ax.axis('equal') # sets donut to be even within frame
		self.ax.set_title("{0}{1}".format(self.stat, self.statType), fontsize=self.statFontSize, y=0.425) # main chart title

	def update(self, i):
		self.stat = self.getStat() # function that returns up-to-date stat
		if self.stat != self.old_stat: # rerenders donut if the stat has changed, otherwise no update
			self.ax.clear() # clears donut before rerendering -- otherwise it builds layers indefinitely
			self.createAxis() # recreate axis
			self.createDonut() # create new donut with new stat
			self.fig.suptitle(self.supTitle, fontsize=self.supFontSize, x=self.supXPos, y=self.supYPos) # super chart title
			self.old_stat = self.stat # updates old stat

if __name__ == '__main__':
	print ('Please launch GUI')
