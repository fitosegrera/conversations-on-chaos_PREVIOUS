#!/usr/bin/env python

#Class to use the espeak TTS engine with python
#Author: fito_segrera / http://fii.to

import os

class Conversation:

	def say(self, tosay):
		os.system("espeak " + "\"" + tosay + "\"")