from popupController import ErrorDialogBox


class DragHandler(object):
	def __init__(self, chartObj, appWindow):
		self.dragged = None
		self.appWindow = appWindow
		self.chartObj = chartObj
		self.chartObj.fig.canvas.mpl_connect("pick_event", self.on_pick_event)
		self.chartObj.fig.canvas.mpl_connect("button_release_event", self.on_release_event)
		self.isActive = True

	def on_pick_event(self, event):
		if self.isActive:
			self.dragged = event.artist #Line2D
			self.pick_pos = (event.mouseevent.xdata, event.mouseevent.ydata)
			self.ind = event.ind

			# can't modify first point
			if self.ind[0] == 0:
				self.dragged = None
				ErrorDialogBox(self.appWindow, "Can't modify the first point!")

			# can't modify last point
			elif self.ind[0] == len(self.dragged.get_xdata()) - 1:
				self.dragged = None
				ErrorDialogBox(self.appWindow, "Can't modify the last point!")


	def on_release_event(self, event):
		if self.dragged is not None:
			xdata = self.dragged.get_xdata() # no need to copy the list, since it is used only by the line2D object
			ydata = self.dragged.get_ydata()
			index = self.ind # if two or more points are too close, this tuple contains more than one point. we take the first
			chartObj = self.chartObj

			# can't move point ["index[0]"] outside of chart
			if not event.xdata or not event.ydata:
				ErrorDialogBox(self.appWindow, "Can't move point {0} off of the chart!".format(index[0]))
				return

			xdata[index[0]] = int(xdata[index[0]] + event.xdata - self.pick_pos[0]) #truncate towards zero
			ydata[index[0]] = int(ydata[index[0]] + event.ydata - self.pick_pos[1])
			#print 'new point:', xdata[index], ydata[index]

			self.dragged.set_data([xdata, ydata])
			self.dragged = None
			self.chartObj.fig.canvas.draw()

	def setDragControl(self): self.isActive = not self.isActive
