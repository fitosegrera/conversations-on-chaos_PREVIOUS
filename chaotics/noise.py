import os
import random

class Noise:

	def sinewave(self, period, freq):
		os.system("play -n  synth " + str(period) + " sin " + str(freq))
		#os.system("play -n  synth 5 sin 347")

	def generate(self):
		for i in range(100):
			t1 = random.random() * (0.08 - 0.001) + 0.001
			t2 = random.random() * (0.01 - 0.0001) + 0.0001
			self.sinewave(t1, 8000)
			self.sinewave(t2, 3000)