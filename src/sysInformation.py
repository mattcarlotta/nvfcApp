import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib import animation, style
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from subprocess import check_output
import math
import re

class SystemInformation():
	def __init__(self, builder):
		self.builder = builder
		self.systemInfo()
		self.gpuInfo()

	def getGPUInfo(self):
		gpuInfo = check_output(
			"nvidia-smi --query-gpu=name,driver_version,vbios_version,memory.total,pcie.link.width.current --format=csv | awk 'NR>1' | sed -e 's/, /,/g' | tr -d '\n'",
			shell=True
			).decode('utf-8')
		return gpuInfo.split(",")

	def getHostInfo(self): return check_output("hostnamectl", shell=True).decode('utf-8')

	def getSysInfo(self):
		with open("/etc/os-release") as f: return f.read()


	def plotGPULabels(self, arr):
		for args in arr: self.setLabel(args[0], args[1])


	def plotSysLabels(self, arr, info):
		for args in arr:
			try:
				res = re.search(args[0], info).group(1) # searches thru info (strings) looking for requested pattern
				self.setLabel(args[1], res)
			except:
				continue

	def setLabel(self, widget, res):
		label = self.builder.get_object(widget)
		label.set_markup("<i>{0}</i>".format(res))

	def systemInfo(self):
		sysInfo = self.getSysInfo()
		sysInfo += self.getHostInfo()
		# OS, codename, distro-like, kernel and architecture
		sysLabelArr = [[
			'PRETTY_NAME="(.*?)"\n',
			'userOSLabel',
		],[
			'VERSION_CODENAME=(.*?)\n',
			'userCodenameLabel',
		],[
			'ID_LIKE=(.*?)\n',
			'userDistroLabel',
		],[
			' Kernel: (.*?)\n',
			'userKernelLabel'
		],[
			' Architecture: (.*?)\n',
			'userArchLabel'
		]]
		self.plotSysLabels(sysLabelArr, sysInfo)

	def gpuInfo(self):
		gpuInfo = self.getGPUInfo()

		if len(gpuInfo) == 5:
			gpuInfoLabelArr = [[
				'userProcLabel',
				gpuInfo[0]
			],[
				'userDriverLabel',
				gpuInfo[1]
			],[
				'userVbiosLabel',
				gpuInfo[2]
			],[
				'userTotMemLabel',
				'{0} (~{1}GB)'.format(gpuInfo[3], math.ceil(int(gpuInfo[3].split(" MiB")[0])/1024))
			],[
				'userPciBwLabel',
				'PCI Express {0}x'.format(gpuInfo[4])
			]]
			self.plotGPULabels(gpuInfoLabelArr)


	# closes Chart and stops GPU updating
	def close():
		plt.close('all')

if __name__ == '__main__':
	print ('Please launch GUI')
