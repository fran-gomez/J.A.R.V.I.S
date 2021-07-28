import subprocess

def cmd (cmdAndArgs, return_output = False):
	cmdProcess = subprocess.run(cmdAndArgs, capture_output = return_output)

	return str(cmdProcess.stdout)

class mimic:

	def __init__(self):
		self.mimicVoicesDir = '../data/mimic_voices/'
		self.updateListsOfVoices()
		self.setVoice('cmu_us_clb.flitevox')
		self.setSpeed(1)

	def updateListsOfVoices(self):
		self.mimicNativeVoices = self.listNativeVoices()
		self.mimicDirVoices = self.listDirVoices()
		self.allMimicVoices = self.mimicNativeVoices + self.mimicDirVoices

	def say(self, *args):
		for string in args:
			cmd(['mimic', '--setf', f'duration_stretch={self.speed}', '-t', string, '-voice', self.voice])

	def listDirVoices(self):
		# Clean output of the ls command
		listDir = cmd(['ls', self.mimicVoicesDir], True)[2:-3]

		# Convert the ls output to a list
		dirVoicesList = listDir.split('\\n')

		return dirVoicesList

	def listNativeVoices(self):
		# Clean output of the command
		voices = cmd(['mimic', '-lv'], True)[2:-1]

		endVoicesString = voices.find('\\')-1

		# Erase the fist part of the output and convert it to a list
		nativeVoicesList = voices[18:endVoicesString].split(' ')

		return nativeVoicesList

	def isNativeVoice(self, voice):
		isNativeVoice = False

		if voice in self.mimicNativeVoices:
			isNativeVoice = True

		return isNativeVoice

	def setVoice(self, voice):
		if  self.isNativeVoice(voice):
			self.voice = voice
		else:
			self.voice = self.mimicVoicesDir + voice
	
	def setSpeed(self, speed):
		self.speed = speed