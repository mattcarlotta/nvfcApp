from subprocess import *
import time
import threading
from curveController import Curve
from threadController import StoppableThread


class NvidiaFanController(StoppableThread):
	""" Class Variables """
	drv_ver = None
	fanspeed = 0
	old_fanspeed = 0
	pause_updates = False
	temp = 0
	""" --------------- """

	def __init__(self, *args, **kwargs):
		super(NvidiaFanController, self).__init__()
		self.lock = threading.Lock() # returns a lock object
		self.drv_ver = self.getDriverVersion() # sets current driver version
		NvidiaFanController.drv_ver = self.drv_ver
		self.drv_ver_change = 352.09 # from this version on, we need to use a different method to change fan speed
		self.drv_ver_regressions = [349.16, 349.12] # can't control fan speed in these driver versions

		if len(args) == 1: self.curve = Curve(args[0]) #[[temp0, speed0], [temp1, speed1], [temp2, speed2]]
		if len(args) == 2: self.curve = Curve(args[0], args[1]) #[[temp0, temp1, temp2], [speed0, speed1, speed2]]

	# resets fan control back to driver
	def disableFanControl(self=None):
		process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=0", shell=True, stdin=PIPE, stdout=PIPE)

	# grabs the GPU driver as a string and returns a float
	def getDriverVersion(self=None):
		try:
			driver_version = check_output("nvidia-smi --query-gpu=driver_version --format=csv | tail -n +2", shell=True)
			return float(driver_version[:-4])
		except:
			return None

	# grabs current fan speed
	def getFanSpeed(self):
		try:
			curr_fspd = check_output("nvidia-smi --query-gpu=fan.speed --format=csv,noheader", shell=True)
			return int(curr_fspd[:3])
		except:
			return None

	# grabs current temp
	def getTemp(self):
		try:
			curr_temp = check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader", shell=True)
			return int(curr_temp)
		except:
			return None

	# whether or not to pause "run" loop
	def pauseUpdates(bool): NvidiaFanController.pause_updates = bool

	# resets old fanspeed to 0 to intiate an update
	def resetFanControl(): NvidiaFanController.old_fanspeed = 0

	# if app is running, control GPU fan
	def run(self):
		while(self.running()):
			if (NvidiaFanController.pause_updates):
				time.sleep(1.0)
				continue # pause loop to update curve points or disable chart
			else:
				self.updateFan() # update fan if needed
				time.sleep(1.0)

		# exit app and reset GPU to auto
		self.disableFanControl()

	# updates old x,y curve points with current curve x,y points
	def setCurve(self, *args, **kwargs):
		if len(args) == 1: self.curve.set(args[0]) # triggered by resetData/openFile ([arr, arr])
		if len(args) == 2: self.curve.set(args[0], args[1]) # triggered by applyData ([arr], [arr])

	# determines how to set the GPU fan speed according to driver
	def setFanSpeed(self, speed):
		# check if driver version is later than 352.09
		if self.drv_ver >= self.drv_ver_change:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUTargetFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

		# else use alternative update GPU control method (GPUCurrent (old) =>  GPUTarget (newer))
		else:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUCurrentFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

	# updates temp and fanspeed only on temp change or applied curve updates
	def updateFan(self):
		old_fspd = NvidiaFanController.old_fanspeed

		# driver version is present and valid
		if self.drv_ver and not self.drv_ver in self.drv_ver_regressions:

			# get current GPU temp
			NvidiaFanController.temp = self.getTemp()
			curr_temp = NvidiaFanController.temp

			# set temp based upon curve fspd point
			NvidiaFanController.fanspeed = self.curve.evaluate(curr_temp)
			curr_fspd = NvidiaFanController.fanspeed

			# checks if the current temp has changed from the stored temp
			if (old_fspd != curr_fspd):
				self.setFanSpeed(curr_fspd) # sets new fan speed according to curve points
				NvidiaFanController.old_fanspeed = curr_fspd # updates an old fspd to compare against an incoming new fspd

		# missing driver version or if driver version is 349.16 or 349.12, stops thread
		else: self.stop()

if __name__ == "__main__":
	print ("Please launch nvda-contrl.py")
