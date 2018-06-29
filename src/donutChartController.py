import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class DonutChart():
    def __init__(self, *args):
        self.box = args[0]
        self.radius, self.width = args[1]
        self.getStat = args[2]
        self.supTitle = args[3]
        self.supXPos, self.supYPos = args[4]
        self.stat = self.getStat()
        self.maxStat = args[5]
        self.statType = args[6]
        self.statFontSize, self.supFontSize = args[7]
        self.cnvsHeight, self.cnvsWidth = args[8]
        self.animDelay = args[9]
        self.a = plt.cm.Blues # fill color
        self.b = plt.cm.Greys # negative color
        self.fig, self.ax = plt.subplots(1) # sets a single subsplot
        self.fig.patch.set_facecolor('white') # sets background to white
        self.donut, _ = self.ax.pie([self.stat, self.maxStat-self.stat], radius=self.radius, colors=[self.a(0.6), self.b(0.6)], counterclock=False, startangle=180)
        plt.setp(self.donut, width=0.2, edgecolor='white') # sets the circle width and adds a white border color
        self.ax.axis('equal') # sets circle to be even within frame
        self.canvas = FigureCanvas(self.fig) # attach fig to a canvas
        self.canvas.set_size_request(self.cnvsHeight, self.cnvsWidth) # sets canvas size
        self.box.add(self.canvas) # adds canvas to specified gtkBox
        self.anim = animation.FuncAnimation(self.fig, self.update, interval=1000, blit=True) # runs animation to update stats


    def update(self, i):
        self.stat = self.getStat()
        self.ax.set_title("{0}{1}".format(self.stat, self.statType), fontsize=self.statFontSize, y=0.425) # main chart title
        self.fig.suptitle(self.supTitle, fontsize=self.supFontSize, x=self.supXPos, y=self.supYPos) # super chart title
        # creates a donut chart with opts: [stat, total-stat], circle radius, colors [blue, grey], grows clockwise at 180 degrees
        self.donut, _ = self.ax.pie([self.stat, self.maxStat-self.stat], radius=self.radius, colors=[self.a(0.6), self.b(0.6)], counterclock=False, startangle=180)
        plt.setp(self.donut, width=0.2, edgecolor='white') # sets the circle width and adds a white border color
        # self.fig.canvas.draw() # draws new updates
