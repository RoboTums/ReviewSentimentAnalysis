#@author tumas rackaitis

#loads course objects from json

def parseJson(jsonFileName='courseData.json'):
	from classCenJson import classCentralDecoder
	import json

	with open(jsonFileName,'r') as readFile:
		data = json.load(readFile)
	dec = classCentralDecoder()

	allCourses = [dec.decodeJsonString(i) for i in data]
	return allCourses
#parseJson()