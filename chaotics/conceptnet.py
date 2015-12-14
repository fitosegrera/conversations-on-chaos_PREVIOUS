#!/usr/bin/env python

#Class to access and work with MIT's ConceptNet web API
#Author: fito_segrera / http://fii.to
#More info about ConceptNet: http://conceptnet5.media.mit.edu/

import json
import urllib2
import time

class ConceptNet:

	def __init__(self):
		self.url = "http://conceptnet5.media.mit.edu/data/5.4/"

	def urlopen_with_retry(self, data):
		response = None
		max_attempts=10
		r=0
		while response is None and r < max_attempts:
			try:
				print ""
				print "Fetching Data..."
				print ""
			 	response = urllib2.urlopen(data)
			except urllib2.URLError:
				r += 1
				print "Re-trying, attempt -- ",r
				time.sleep(5)
				pass

		return response

	def lookup(self, lang, term, verbose):
		toReturn = None
		url_to_search = self.url + "c/" + lang + "/" + term + "?offset=5&limit=6"
		data = self.urlopen_with_retry(url_to_search)
		json_data = json.load(data)
		print url_to_search
		termCount = 0
		print ""
		print "TERM:", term
		print ""
		print "////////////////////////////////////"
		for i in json_data["edges"]:
			if verbose:
				print "----------------"
				print i["end"]
				print "relation:", i["rel"]
				print i["surfaceEnd"]
				print i["surfaceStart"]
				print "weight:", i["weight"]

			if len(i["end"]) > (len("/c/en/")+len(term)):
				parsed = self.splitter(json_data["edges"][0]["end"])
				print "#################"
				print parsed
				print "#################"
				return parsed
				break

	def relation(self, rel, concept, verbose):
		url_to_search = self.url + "search?rel=/r/" + rel +"&end=/c/en/" + concept
		data = self.urlopen_with_retry(url_to_search)
		json_data = json.load(data)
		print url_to_search
		for i in json_data["edges"]:
			if verbose:
				print "----------------"
				print i["surfaceEnd"]
				print i["surfaceStart"]
				print "weight:", i["weight"]

	def termsAssociation(self, term1, term2, limit, weight, lang, verbose):
		toReturn = []
		url_to_search = self.url + "assoc/list/en/" + term1 + "," + term2 +"@"+ str(weight) +"?limit=" + str(limit) + "&filter=/c/" + lang
		data = self.urlopen_with_retry(url_to_search)
		json_data = json.load(data)
		
		print ""
		print "////////////////////////////////////"
		print url_to_search
		for i in json_data["similar"]:
			print "----------------"
			termCount = 0
			for j in i:
				if termCount==0:
					parsed = j.split("/c/en/")
					toReturn.append(parsed[1])
				print j
				termCount += 1

		return toReturn

	def splitter(self, data):
		split = None
		for char in range(len(data)):
			index = len(data)-1-char
			if index >= 0:
				if data[index] == '/':
					print "****************"
					print char
					split = data[index+1:len(data)]
					break
		return split

