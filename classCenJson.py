import pandas as pd 
import json
from classCentralCourse import classCentralCourse
class classCentralEncoder(json.JSONEncoder):
	def defaultEncode(self,course):
		if isinstance(course,classCentralCourse):
			json = { 
				'name' = course.name,
		        'relatedCourses' = course.relatedCourses,
		        'description' =course.description,
		        'reviews'= course.reviews.to_json(orient='split'),
		        'institution'= course.institution,
		        'provider' =course.provider,
		        'attributes'= course.attributes,
		        'url'= course.url = url,
		        'numAdditionalInfo'=course.numAdditionalInfo,
	        }
	        return json
	    else:
	    	super().default(self,course)
	