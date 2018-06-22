from subprocess import *
import time
import os
import threading
from messageController import displayDialogBox, displayErrorBox


class Curve():
	def __init__(self, *args, **kwargs):
		if len(args) == 1: #[[temp0, speed0], [temp1, speed1], [temp2, speed2]]
			self.cpa = list(args[0])
		if len(args) == 2: #[[temp0, temp1, temp2], [speed0, speed1, speed2]]
			self.convertIntoMatrix(args[0], args[1])

	def convertIntoMatrix(self, x_values, y_values):
		self.cpa = list()
		x_temp = list(x_values)
		y_speed = list(y_values)
		for index in range(0, len(x_temp)):
			self.cpa.append([x_temp[index], y_speed[index]])

	def evaluate(self, x):
		point_i = 0
		while(point_i < len(self.cpa) - 1 and x):
			if(self.cpa[point_i][0] <= x and self.cpa[point_i + 1][0] > x):
				point_1 = self.cpa[point_i]
				point_2 = self.cpa[point_i + 1]
				delta_x = point_2[0] - point_1[0]
				delta_y = point_2[1] - point_1[1]

				gradient = float(delta_y)/float(delta_x)

				x_bit = x - point_1[0]
				y_bit = int(float(x_bit) * gradient)
				y = point_1[1] + y_bit
				return y

			point_i += 1

	def setCurve(self, *args, **kwargs):
		if len(args) == 1:
			self.cpa = list(args[0])
		if len(args) == 2:
			self.convertIntoMatrix(args[0], args[1])


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self.stop_thread = threading.Event()

    def stop(self):
        self.stop_thread.set()

    def stopped(self):
        return self.stop_thread.isSet()

class NvidiaFanController(StoppableThread):

	""" Class Variables """
	DRIVER_VERSION_CHANGE = 352.09 #from this version on, we need to use a different method to change fan speed
	DRIVER_VERSIONS_ERROR = [349.16, 349.12] #cannot control fan speed in these driver versions
	drv_ver = 0
	fanspeed = 0
	old_fanspeed = 0
	pause_updates = False
	temp = 0
	""" --------------- """

	def __init__(self, *args, **kwargs):
		super(NvidiaFanController, self).__init__()
		self.curve_lock = threading.Lock()

		if len(args) == 1: #[[temp0, speed0], [temp1, speed1], [temp2, speed2]]
			self.curve = Curve(args[0])
		if len(args) == 2: #[[temp0, temp1, temp2], [speed0, speed1, speed2]]
			self.curve = Curve(args[0], args[1])

	def disableFanControl(self=None):
		process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=0", shell=True, stdin=PIPE, stdout=PIPE)

	# grabs the GPU driver as a string and returns a float
	def getDriverVersion(self):
		try:
			driver_version = check_output("nvidia-smi --query-gpu=driver_version --format=csv | tail -n +2", shell=True)
			return float(driver_version[:-4])
		except:
			return None

	# grab current fan speed
	def getFanSpeed(self):
		try:
			output = check_output("nvidia-smi --query-gpu=fan.speed --format=csv,noheader", shell=True)
			curr_fspd = int(output[:3])
			return curr_fspd
		except:
			return None

	# grab current temp
	def getTemp(self):
		try:
			output = check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader", shell=True)
			curr_temp = int(output)
			return curr_temp
		except:
			return None

	def pauseUpdates(bool): NvidiaFanController.pause_updates = bool

	def resetFanControl(): NvidiaFanController.old_fanspeed = 0

	# if app is running, control GPU fan
	def run(self):
		while(not self.stopped()):
			if (NvidiaFanController.pause_updates):
				time.sleep(1.0)
				continue # pause loop to update curve points or disable chart
			else:
				self.updateFan() # update fan if needed
				time.sleep(1.0)

		# exit app and reset GPU to auto
		self.disableFanControl()
		return

	def setCurve(self, *args, **kwargs):
		self.curve_lock.acquire()
		# print "Fan Speed Curve updated"

		if len(args) == 1:
			self.curve.setCurve(args[0])

		if len(args) == 2:
			self.curve.setCurve(args[0], args[1])

		self.curve_lock.release()

	def setFanSpeed(self, speed):
		NvidiaFanController.drv_ver = self.getDriverVersion()
		drv_ver = NvidiaFanController.drv_ver

		if not drv_ver:
			self.stop()

		# check if driver version is larger than 352.09
		elif drv_ver >= NvidiaFanController.DRIVER_VERSION_CHANGE:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUTargetFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

		# if driver is 349.16 or 349.12 exit app
		elif drv_ver in NvidiaFanController.DRIVER_VERSIONS_ERROR:
			displayDialogBox("Can't control fan speed in driver version {0}. Please update your driver to use this app.".format(drv_ver))
			self.stop()

		# else use alternative update GPU control method (GPUCurrent (old) =>  GPUTarget (newer))
		else:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUCurrentFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

	def updateFan(self):
		old_fspd = NvidiaFanController.old_fanspeed

		self.curve_lock.acquire() # get Curve thread

		NvidiaFanController.temp = self.getTemp() # get current GPU temp
		curr_temp = NvidiaFanController.temp

		NvidiaFanController.fanspeed = self.curve.evaluate(curr_temp) # set temp based upon curve fspd point
		curr_fspd = NvidiaFanController.fanspeed

		"""
		Check if the fspd needs to be updated because of temp change or because of curve point update
		No need to hammer the GPU with updates if nothing has changed
		"""
		if (old_fspd != curr_fspd):
			self.setFanSpeed(curr_fspd) # sets new fan speed according to curve points
			NvidiaFanController.old_fanspeed = curr_fspd # updates an old fspd to compare against an incoming new fspd

		self.curve_lock.release()

if __name__ == "__main__":
	print ("Please launch nvda-contrl.py")
