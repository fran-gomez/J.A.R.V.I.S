import subprocess


def cmd (cmdAndArgs, returnOutput = False):
	cmdProcess = subprocess.run(cmdAndArgs, capture_output = returnOutput)

	return str(cmdProcess.stdout)


class Mimic:

	"""Basic interaction with the mimic TTS engine."""

	def __init__(self):
		self.mimicVoicesDir = '../data/mimic_voices/'
		self.update_list_of_voices()
		self.set_voice('cmu_us_clb.flitevox')
		self.set_speed(1)

	def update_list_of_voices(self):
		self.mimicNativeVoices = self.list_native_voices()
		self.mimicDirVoices = self.list_dir_voices()
		self.allMimicVoices = self.mimicNativeVoices + self.mimicDirVoices

	def say(self, *args):
		for string in args:
			cmd(['mimic', '--setf', f'duration_stretch={self.speed}', '-t', string, '-voice', self.voice])

	def list_dir_voices(self):
		# Clean output of the ls command
		listDir = cmd(['ls', self.mimicVoicesDir], True)[2:-3]

		# Convert the ls output to a list
		dirVoicesList = listDir.split('\\n')

		return dirVoicesList

	def list_native_voices(self):
		# Clean output of the command
		voices = cmd(['mimic', '-lv'], True)[2:-1]

		endVoicesString = voices.find('\\')-1

		# Erase the fist part of the output and convert it to a list
		nativeVoicesList = voices[18:endVoicesString].split(' ')

		return nativeVoicesList

	def is_native_voice(self, voice):
		isNativeVoice = False

		if voice in self.mimicNativeVoices:
			isNativeVoice = True

		return isNativeVoice

	def set_voice(self, voice):
		if  self.is_native_voice(voice):
			self.voice = voice
		else:
			self.voice = self.mimicVoicesDir + voice
	
	def set_speed(self, speed):
		self.speed = speed