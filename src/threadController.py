import threading


# allows the NvidiaFanController to continually run
class StoppableThread(threading.Thread):
	def __init__(self):
		super().__init__() # this allows us to pass parent methods to child class (eg. NvidiaFanController => self.stop())
		self.thread = threading.Event() # initialize a thread
		self.thread.set() # set the thread to true

	# check if thread is still running, returns bool (true)
	def running(self): return self.thread.is_set()

	# stops thread by setting the thread to false
	def stop(self): self.thread.clear()
