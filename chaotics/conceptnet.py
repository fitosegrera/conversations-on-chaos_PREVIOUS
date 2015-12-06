#!/usr/bin/env python

#Class to access and work with MIT's ConceptNet web API
#Author: fito_segrera / http://fii.to
#More info about ConceptNet: http://conceptnet5.media.mit.edu/

import json
import urllib2

class ConceptNet:

	def __init__(self):
		self.url = "http://conceptnet5.media.mit.edu/data/5.4/"

	def urlopen_with_retry(self, data):
		response = None
		max_attempts=10
		r=0
		while response is None and r < max_attempts:
			try:
			 	response = urllib2.urlopen(data)
			except urllib2.URLError:
				r=r+1
				print "Re-trying, attempt -- ",r
				time.sleep(5)
				pass

		return response

	def lookup(self, lang, term, verbose):
		toReturn = None
		url_to_search = self.url + "c/" + lang + "/" + term
		data = self.urlopen_with_retry(url_to_search)
		json_data = json.load(data)
		print url_to_search
		termCount = 0
		for i in json_data["edges"]:
			if verbose:
				print "----------------"
				print i["end"]
				print "relation:", i["rel"]
				print i["surfaceEnd"]
				print i["surfaceStart"]
				print "weight:", i["weight"]
			if i["rel"] == "/r/IsA":
				parsed = i["end"].split("/n/")
				if len(parsed) < 1:
					tmpstr = parsed[1]
					for ch in tmpstr:
						if ch == "_":
							 tmpstr=tmpstr.replace(ch, " ")
					toReturn = tmpstr
					break

			if termCount >= len(json_data["edges"]) - 1:
				toReturn = None

			termCount += 1

		return toReturn


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