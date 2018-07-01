import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pylab as plt
from matplotlib import animation, style
from subprocess import check_output
import math
import re
from donutChartController import DonutChart
from fanController import FanController

class SystemInformation():
	def __init__(self, builder):
		self.builder = builder
		self.systemInfo() # System Information
		self.gpuInfo() # GPU Information
		# GPU utilization (load)
		self.gpuUtil1 = DonutChart(
			self.builder.get_object("gpuUsageBox"), # gtkBox
			[1.4, 0.15], # donut radius and width
			self.getUtilization, # current GPU utilization stat
			'load', # suptitle
			[0.512, 0.420], # suptitle placement x,y coords
			100, # max stat
			'%', # type of stat
			[16,12], # label font sizes
			[300, 280] # canvas width and height
		)
		# GPU clock
		self.gpuUtil2 = DonutChart(
			self.builder.get_object("gpuClockBox"),
			[1.3, 0.1],
			self.getClock,
			'clock',
			[0.512, 0.420],
			int(self.gpuInfo[4].replace("MHz", '')),
			'MHz',
			[12,10],
			[150, 175]
		)
		# GPU memory
		self.gpuUtil3 = DonutChart(
			self.builder.get_object("gpuMemBox"),
			[1.3, 0.1],
			self.getMem,
			'memory',
			[0.512, 0.420],
			int(self.gpuInfo[2].replace("MiB", '')),
			'MiB',
			[12,10],
			[150, 175]
		)
		# GPU temperature
		self.gpuStat1 = DonutChart(
			self.builder.get_object("gpuTempBox"),
			[1.3, 0.1],
			self.getTemp,
			'temp',
			[0.512, 0.420],
			100,
			'°C',
			[14,10],
			[300, 150]
		)
		# GPU fan speed
		self.gpuStat2 = DonutChart(
			self.builder.get_object("gpuFspdBox"),
			[1.3, 0.1],
			self.getFanSpeed,
			'fan',
			[0.512, 0.420],
			100,
			'%',
			[14,10],
			[300, 150]
		)
		# GPU power draw
		self.gpuStat3 = DonutChart(
			self.builder.get_object("gpuPowerBox"),
			[1.3, 0.1],
			self.getFanSpeed,
			'power',
			[0.512, 0.420],
			float(self.gpuInfo[5].replace("W", '')),
			'W',
			[14,10],
			[300, 150]
		)

	# command-line shell command returns output
	def getGpuInfoByString(self, string):
		try:
			info = check_output(string, shell=True).decode('utf8')
			return int(info)
		except:
			return 0

	# grabs current clock speed
	def getClock(self):
		return self.getGpuInfoByString("nvidia-smi --query-gpu=clocks.current.graphics --format=csv,noheader | sed 's/[^0-9]*//g'")

	# grabs current fan speed
	def getFanSpeed(self):
		return self.getGpuInfoByString("nvidia-smi --query-gpu=fan.speed --format=csv,noheader | sed 's/[^0-9]*//g'")

	# grabs current memory usage
	def getMem(self):
		return self.getGpuInfoByString("nvidia-smi --query-gpu=memory.used --format=csv | awk 'NR>1' | sed 's/[^0-9]*//g'")

	# grabs current power draw
	def getPower(self):
		try:
			power_draw = check_output("nvidia-smi --query-gpu=power.draw --format=csv | awk 'NR>1' | sed 's/[^0-9.]*//g'", shell=True).decode('utf8')
			return float(power_draw)
		except:
			return 0

	# grabs current temp
	def getTemp(self):
		return self.getGpuInfoByString("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader")

	# grabs current graphics usage
	def getUtilization(self):
		return self.getGpuInfoByString("nvidia-smi --query-gpu=utilization.gpu --format=csv | awk 'NR>1' |  sed 's/[^0-9]*//g;'")

	# grabs processor, driver, total memory, pci link speed, max clock speed, and max power draw
	def getGPUInfo(self):
		try:
			gpuInfo = check_output(
				"nvidia-smi --query-gpu=name,driver_version,memory.total,pcie.link.width.current,clocks.max.graphics,power.limit --format=csv | awk 'NR>1' | sed -e 's/, /,/g' | tr -d '\n'",
				shell=True
				).decode('utf-8')
			return gpuInfo.split(",")
		except:
			return 0

	# grabs kernel and architecture
	def getHostInfo(self):
		try:
			hostInfo = check_output("hostnamectl", shell=True).decode('utf-8')
			return hostInfo
		except:
			return None

	# grabs system info
	def getSysInfo(self):
		try:
			with open("/etc/os-release") as f:
				return f.read()
		except:
			return None

	# plots GPU labels
	def plotGPULabels(self, arr):
		for args in arr: self.setLabel(args[0], args[1])

	# plot Sys labels
	def plotSysLabels(self, arr, info):
		for args in arr:
			try:
				res = re.search(args[0], info).group(1) # searches thru info (strings) looking for requested pattern
				self.setLabel(args[1], res)
			except:
				continue

	# sets labels
	def setLabel(self, widget, res):
		label = self.builder.get_object(widget)
		label.set_markup("<i>{0}</i>".format(res))

	# gets system info for labels
	def systemInfo(self):
		sysInfo = self.getSysInfo()
		sysInfo += self.getHostInfo()
		# OS, codename, distro-like, kernel and architecture
		if sysInfo:
			sysLabelArr = [
				['PRETTY_NAME="(.*?)"\n', 'userOSLabel'],
				['VERSION_CODENAME=(.*?)\n','userCodenameLabel'],
				['ID_LIKE=(.*?)\n', 'userDistroLabel'],
				[' Kernel: (.*?)\n', 'userKernelLabel'],
				[' Architecture: (.*?)\n','userArchLabel']
			]
			self.plotSysLabels(sysLabelArr, sysInfo)

	# gets gpuinfo for labels
	def gpuInfo(self):
		self.gpuInfo = self.getGPUInfo()

		if len(self.gpuInfo) == 6:
			gpuInfoLabelArr = [
				['userProcLabel',self.gpuInfo[0]],
				['userDriverLabel', self.gpuInfo[1]],
				['userTotMemLabel', '{0} (~{1}GB)'.format(self.gpuInfo[2], math.ceil(int(self.gpuInfo[2].split(" MiB")[0])/1024))],
				['userPciBwLabel','PCI Express {0}x'.format(self.gpuInfo[3])],
				['userMaxClockLabel', self.gpuInfo[4]],
				['userPwrDrawLabel', self.gpuInfo[5]]
			]
			self.plotGPULabels(gpuInfoLabelArr)

if __name__ == '__main__':
	print ('Please launch GUI')
