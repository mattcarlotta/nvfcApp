from subprocess import *
import time
import threading
from curveController import Curve
from threadController import StoppableThread


class FanController(StoppableThread):
	""" Class Variables """
	fanspeed = 0
	temp = 0
	""" --------------- """

	def __init__(self, xdata, ydata):
		super().__init__()
		self.lock = threading.Lock() # intialize a lock object (allows more control over self.run() updates)
		self.drv_ver = self.getDriverVersion() # sets current driver version
		self.drv_ver_change = 352.09 # from this version on, we need to use a different method to change fan speed
		self.drv_ver_regressions = [349.16, 349.12] # can't control fan speed in these driver versions
		self.old_fspd = 0 # initialize an old fanspeed for later comparison
		self.curve = Curve(xdata, ydata) #[[temp0, temp1, temp2], [speed0, speed1, speed2]]

	# resets fan control back to driver
	def disableFanControl(self):
		process = Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=0", shell=True, stdin=PIPE, stdout=PIPE)

	# grabs the GPU driver as a string and returns a float
	def getDriverVersion(self):
		try:
			driver_version = check_output("nvidia-smi --query-gpu=driver_version --format=csv | tail -n +2", shell=True).decode('utf8')
			# return 349.16
			return float(driver_version[0:6])
		except:
			return None

	# retrieves current loaded driver version
	def getLoadedDriver(self): return self.drv_ver

	# grabs current temp
	def getTemp(self):
		try:
			curr_temp = check_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader", shell=True)
			return int(curr_temp)
		except:
			return None

	# pauses "run" loop
	def pause(self): self.lock.acquire() # locks the thread (blocking any calls to acquire it)

	# resumes "run" loop
	def resume(self): self.lock.release() # unlocks the thread (unblocking any calls to acquire it)

	# resets old fanspeed to 0 to intiate an update
	def resetFanControl(self): self.old_fspd = 0

	# if app is running, control GPU fan
	def run(self):
		while(self.running()):
			self.lock.acquire() # locks the thread (if thread is already locked, skips try)
			try:
				self.updateFan() # update fan if needed
				self.lock.release() # releases the thread
			except: pass # sometimes self.lock.release triggers runtime error if stopped prematurely
			finally: time.sleep(1.0) # sleeps for 1s

		# if thread is stopped, exit app and reset GPU to auto
		self.disableFanControl()

	# updates old x,y curve points with current curve x,y points (either [xdata, ydata] or [xdata], [ydata])
	def setCurve(self, *args): self.curve.set(args[0]) if len(args) == 1 else self.curve.set(args[0], args[1])

	# determines how to set the GPU fan speed according to driver
	def setFanSpeed(self, speed):
		gpuString = 'Target' if self.drv_ver >= self.drv_ver_change else 'Current' # dvr vers > 352.09 (use GPUTargetFanSpeed else GPUCurrentFanSpeed)
		Popen("nvidia-settings -a [gpu:0]/GPUFanControlState=1 -a [fan:0]/GPU{0}FanSpeed={1}".format(gpuString, speed), shell=True, stdin=PIPE, stdout=PIPE)

	# stops any locked event threading
	def stopUpdates(self):
		self.stop() # stops thread
		self.lock.acquire(False) # override and unlock any thread blocking
		self.lock.release() # release the thread to be stopped

	# updates temp and fanspeed only on temp change or applied curve updates
	def updateFan(self):
		if self.drv_ver and not self.drv_ver in self.drv_ver_regressions: # driver version is present and valid
			curr_temp = FanController.temp = self.getTemp() # get current GPU temp
			curr_fspd = FanController.fanspeed = self.curve.evaluate(curr_temp) # set temp based upon curve fspd point
			# checks if the current temp has changed from the stored temp
			if (self.old_fspd != curr_fspd):
				self.setFanSpeed(curr_fspd) # sets new fan speed according to curve points
				self.old_fspd = curr_fspd  # updates an old fspd to compare against an incoming pssible new fspd
		# missing dvr vers or if dvr vers is 349.16 or 349.12, stops thread
		else: self.stop()

if __name__ == "__main__":
	print ("Please launch nvda-contrl.py")
