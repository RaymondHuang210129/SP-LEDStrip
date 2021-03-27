import subprocess as sp
import signal

class SubProcessHandler:
	def __init__(self):
		self.__subp = None
		self.__modes = dict()
		self.__actionResult = False
		try:
			with open('modeConfig.txt', 'r') as configFile:
				configs = configFile.readlines()
				for config in configs:
					self.__modes.update({config.split()[0]: config.split()[1:]})
			self.__actionResult = True
		except Exception as e:
			print(e)
			self.__actionResult = False

#	def __del__(self):
#		self.terminateProcess()

	def createProcess(self, mode):
		if mode in self.__modes.keys():
			try:
				if not self.__isTerminated():
					self.__subp.terminate()
					self.__subp.wait()
				self.__subp = sp.Popen(self.__modes[mode])
				self.__actionResult = True
			except Exception as e:
				print(e)
				self.__actionResult = False
		else:
			self.__actionResult = False
		

	def terminateProcess(self):
		try:
			if not self.__isTerminated():
				self.__subp.send_signal(signal.SIGINT)
				self.__subp.wait()
			self.__actionResult = True
		except Exception as e:
			print(e)
			self.__actionResult = False

	def __isTerminated(self):
		if self.__subp and self.__subp.returncode == None:
			return False
		else:
			return True

	def isActionSuccess(self):
		return self.__actionResult


if __name__ == '__main__':
	try:
		print('ProcessHandler debug test')
		subProcessHandler = SubProcessHandler()
		while True:
			command = input('Command: ')
			if command == 'c':
				subProcessHandler.createProcess('clock')
			elif command == 't':
				subProcessHandler.terminateProcess()
			elif command == 'w':
				subProcessHandler.createProcess('white')
			elif command == 'r':
				subProcessHandler.createProcess('rainbow')
	except KeyboardInterrupt:
		pass






