import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class DonutChart():
    def __init__(self, gpuBox):
        self.stat = 1
        self.a = plt.cm.Blues # fill color
        self.b = plt.cm.Greys # negative color
        self.fig, self.ax = plt.subplots(1) # sets a single subsplot
        self.fig.patch.set_facecolor('white') # sets background to white
        self.donut, _ = self.ax.pie([self.stat, 100-self.stat], radius=1.3, colors=[self.a(0.6), self.b(0.6)], counterclock=False, startangle=180)
        plt.setp(self.donut, width=0.2, edgecolor='white') # sets the circle width and adds a white border color
        self.ax.axis('equal') # sets circle to be even within frame
        self.canvas = FigureCanvas(self.fig) # attach fig to a canvas
        self.canvas.set_size_request(200, 200) # sets canvas size
        gpuBox.add(self.canvas) # adds canvas to specified gtkBox
        self.anim = animation.FuncAnimation(self.fig, self.update, interval=1000) # runs animation to update stats


    def update(self, i):
        self.ax.set_title("{0}%".format(self.stat), fontsize=16, y=0.425) # Chart's title
        # creates a donut chart with opts: [stat, total-stat], circle radius, colors [blue, grey], grows clockwise at 180 degrees
        self.donut, _ = self.ax.pie([self.stat, 100-self.stat], radius=1.3, colors=[self.a(0.6), self.b(0.6)], counterclock=False, startangle=180)
        plt.setp(self.donut, width=0.2, edgecolor='white') # sets the circle width and adds a white border color
        if self.stat > 0 and self.stat < 10: self.stat += 1
        else: self.stat = 1
        self.fig.canvas.draw() # draws new updates
