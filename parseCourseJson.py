#@author tumas rackaitis

#loads course objects from json

def parseJson():
	from classCenJson import classCentralDecoder
	import json

	with open('courseData.json','r') as readFile:
		data = json.load(readFile)
	dec = classCentralDecoder()

	allCourses = [dec.decodeJsonString(i) for i in data]
	return allCourses
parseJson()