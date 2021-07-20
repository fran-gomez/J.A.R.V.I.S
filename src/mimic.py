import subprocess

class mimic:

	def __init__(self):
		self.mimicVoicesDir = "../mimic_voices/"
		self.mimicNativeVoices = self.listNativeVoices()
		self.mimicDirVoices = self.listDirVoices()
		self.allMimicVoices = self.listAllMimicVoices()
		self.voice = self.allMimicVoices[1]

	def say(self, words):
		subprocess.run(["mimic", "-t", words, "-voice", self.voice])

	def listDirVoices(self):
		listDirVoicesProcess = subprocess.run(["ls", self.mimicVoicesDir], capture_output = True)
		listDir = str(listDirVoicesProcess.stdout)[2:-3]

		dirVoicesList = listDir.split("\\n")

		return dirVoicesList

	def listNativeVoices(self):
		listNativeVoicesProcess = subprocess.run(["mimic", "-lv"], capture_output = True)
		voices = str(listNativeVoicesProcess.stdout)[2:-1]

		endVoicesString = voices.find("\\")-1

		nativeVoicesList = voices[18:endVoicesString].split(" ")

		return nativeVoicesList

	def listAllMimicVoices(self):
		return self.listNativeVoices() + self.listDirVoices()

	def isNativeVoice(self, voice):
		isNativeVoice = False

		if voice in self.mimicNativeVoices:
			isNativeVoice = True

		return isNativeVoice

engine = mimic()
engine.say("Hello")
