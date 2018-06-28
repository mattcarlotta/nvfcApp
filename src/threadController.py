import threading


# allows the NvidiaFanController to continually run
class StoppableThread(threading.Thread):
	def __init__(self):
		super().__init__() # this allows us to pass parent methods to child class (eg. NvidiaFanController => self.stop())
		self.event = threading.Event() # initialize an event listener
		self.event.set() # set the thread to true

	# check if thread is still running, returns bool (true)
	def running(self): return self.event.is_set()

	# stops thread by setting it to false
	def stop(self): self.event.clear()
