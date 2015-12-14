#!/usr/bin/env python

from chaotics import conceptnet
from chaotics import conversation
from chaotics import noise
import random
import time

cn = conceptnet.ConceptNet()
speak = conversation.Conversation()
datasound = noise.Noise()

language = "en"
rel = "RelatedTo" #more info at: https://github.com/commonsense/conceptnet5/wiki/Relations
origin = "chaos"
destiny = "order"
weight = 0.001
inc = 0.001
cycle = 0

numberOfWords = 6
words = [None] * numberOfWords

def throwPendulum(w):
	chosen = w[random.randint(0,numberOfWords-1)]
	return chosen

def getWords(initConcept, w):
	data = cn.termsAssociation(initConcept, destiny, 6, w, "en", False)
	return data

def run():
	global origin, weight, inc, cycle
	
	datasound.generate()
	time.sleep(5)

	tosay = cn.lookup(language, origin, True)
	if tosay == None:
		tosay = origin
	print ""
	print "@@@@@@@@@@@@@@@@@@@"
	print "TO SAY:", tosay
	print "@@@@@@@@@@@@@@@@@@@"
	print ""
	speak.say(str(tosay))

	print ""
	print "////////////////////////////////////"
	print "origin: chaos --> destination: order"
	print "cycle:", cycle
	words = getWords(origin, weight)
	print "new words:", words
	origin = throwPendulum(words)
	print "evolved idea:", origin
	print "current edge weight:", weight
	print "////////////////////////////////////"
	print ""

	weight += random.random() * (0.01 - 0.001) + 0.001
	cycle += 1

if __name__ == "__main__":
	try:	
		while True:
			run()
			time.sleep(5)
	except KeyboardInterrupt:
		exit()

	#cn.termsAssociation(origin, destiny, 50, 0.01, "en", True)
	#cn.lookup(language, origin, True)
	#cn.relation(rel, origin, True)