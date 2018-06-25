from subprocess import *
import time
import threading


class Curve():
	def __init__(self, *args, **kwargs):
		if len(args) == 1: self.cpa = list(args[0]) #[[temp0, speed0], [temp1, speed1], [temp2, speed2]]
		if len(args) == 2: self.convertIntoMatrix(args[0], args[1]) #[[temp0, temp1, temp2], [speed0, speed1, speed2]]

	def convertIntoMatrix(self, x_values, y_values):
		self.cpa = list()
		x_temp = list(x_values)
		y_speed = list(y_values)
		for index in range(0, len(x_temp)): self.cpa.append([x_temp[index], y_speed[index]])

	def evaluate(self, x):
		index = 0
		while(index < len(self.cpa) - 1 and x):
			if(self.cpa[index][0] <= x and self.cpa[index + 1][0] > x):
				point_1 = self.cpa[index]
				point_2 = self.cpa[index + 1]
				delta_x = point_2[0] - point_1[0]
				delta_y = point_2[1] - point_1[1]

				gradient = float(delta_y)/float(delta_x)

				x_bit = x - point_1[0]
				y_bit = int(float(x_bit) * gradient)
				y = point_1[1] + y_bit
				return y

			index += 1

	def setCurve(self, *args, **kwargs):
		if len(args) == 1: self.cpa = list(args[0])
		if len(args) == 2: self.convertIntoMatrix(args[0], args[1])


# a thread class with a stop() method -- the thread itself has to check regularly for the stopped() condition.
class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self.stop_thread = threading.Event()

    def stop(self): self.stop_thread.set()

    def stopped(self): return self.stop_thread.isSet()

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
		self.curve_lock = threading.Lock()

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
		while(not self.stopped()):
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
		self.curve_lock.acquire()

		if len(args) == 1: self.curve.setCurve(args[0])
		if len(args) == 2: self.curve.setCurve(args[0], args[1])

		self.curve_lock.release()

	# determines how to set the GPU fan speed according to driver
	def setFanSpeed(self, speed):
		# if missing driver version or if driver version is 349.16 or 349.12, kill fan control
		if not self.drv_ver or self.drv_ver in self.drv_ver_regressions: self.stop()

		# check if driver version is later than 352.09
		elif self.drv_ver >= self.drv_ver_change:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUTargetFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

		# else use alternative update GPU control method (GPUCurrent (old) =>  GPUTarget (newer))
		else:
			process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPUCurrentFanSpeed={0}".format(speed), shell=True, stdin=PIPE, stdout=PIPE)

	# updates temp and fanspeed only on temp change or applied curve updates
	def updateFan(self):
		old_fspd = NvidiaFanController.old_fanspeed

		self.curve_lock.acquire()

		# get current GPU temp
		NvidiaFanController.temp = self.getTemp()
		curr_temp = NvidiaFanController.temp

		# check to see if driver version is present and not regressed
		if self.drv_ver and not self.drv_ver in self.drv_ver_regressions:
			# set temp based upon curve fspd point
			NvidiaFanController.fanspeed = self.curve.evaluate(curr_temp)
			curr_fspd = NvidiaFanController.fanspeed

			# checks if the current temp has changed from the stored temp
			if (old_fspd != curr_fspd):
				self.setFanSpeed(curr_fspd) # sets new fan speed according to curve points
				NvidiaFanController.old_fanspeed = curr_fspd # updates an old fspd to compare against an incoming new fspd

		self.curve_lock.release()

if __name__ == "__main__":
	print ("Please launch nvda-contrl.py")
