import os
import threading

class JumanLauncher(object):
	PATH = r"juman\juman.exe"

	def __init__(self):
		pass

	@staticmethod
	def launch():
		t = threading.Thread(target=os.system,
			args=[JumanLauncher.PATH + " -S"])
		t.start()
