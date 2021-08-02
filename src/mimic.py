import subprocess


def cmd (cmd_and_args, return_output = False):
	cmd_process = subprocess.run(cmd_and_args, capture_output = return_output)

	return str(cmd_process.stdout)


class Mimic:

	"""Basic interaction with the mimic TTS engine."""

	def __init__(self):
		self.mimic_voices_dir = '../data/mimic_voices/'
		self.update_list_of_voices()
		self.set_voice('cmu_us_clb.flitevox')
		self.set_speed(1)

	def update_list_of_voices(self):
		self.mimic_native_voices = self.list_native_voices()
		self.mimic_dir_voices = self.list_dir_voices()
		self.all_mimic_voices = self.mimic_native_voices + self.mimic_dir_voices

	def say(self, *args):
		for string in args:
			cmd(['mimic', '--setf', f'duration_stretch={self.speed}', '-t', string, '-voice', self.voice])

	def list_dir_voices(self):
		# Clean output of the ls command
		list_dir = cmd(['ls', self.mimic_voices_dir], True)[2:-3]

		# Convert the ls output to a list
		dir_voices_list = list_dir.split('\\n')

		return dir_voices_list

	def list_native_voices(self):
		# Clean output of the command
		voices = cmd(['mimic', '-lv'], True)[2:-1]

		end_voices_string = voices.find('\\')-1

		# Erase the fist part of the output and convert it to a list
		native_voices_list = voices[18:end_voices_string].split(' ')

		return native_voices_list

	def is_native_voice(self, voice):
		is_native_voice = False

		if voice in self.mimic_native_voices:
			is_native_voice = True

		return is_native_voice

	def set_voice(self, voice):
		if  self.is_native_voice(voice):
			self.voice = voice
		else:
			self.voice = self.mimic_voices_dir + voice
	
	def set_speed(self, speed):
		self.speed = speed