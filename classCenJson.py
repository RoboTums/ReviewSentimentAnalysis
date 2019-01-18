# @author: Tumas Rackaitis
# This class encodes class central course objects and allows json conversion.
# @usage:
# encoder = classCentralEncoder()
# encodedJson = encoder.encode(courseObject)
# decoder = classCentralDecoder()
#
# class = classCentralDecoder()
#

import pandas as pd
import json
from classCentralCourse import classCentralCourse


class classCentralEncoder(json.JSONEncoder):
    # overrided the standard JSONEncoder's default() method
    def default(self, course, fileCreation=True):
        if isinstance(course, classCentralCourse):
            #print('triggered')
            filename = str(course.name) + '.json'
            jsonReady = {
                'name': course.name,
                'relatedCourses': course.relatedCourses,
                'description': course.description,
                'reviews': course.reviews.to_json(orient='split'),
                'institution': course.institution,
                'provider': course.provider,
                'attributes': course.attributes,
                'url': course.url,
                'numAdditionalInfo': course.numAdditionalInfo,
            }
            if fileCreation:
                with open(filename, 'w') as outfile:
                    json.dump(jsonReady, outfile)
                    
            return jsonReady
        else:
            super().default(self, course)


# decodes course from json
class classCentralDecoder:
        # takes in json file name
    def decodeJson(self,Json):
        decoded = classCentralCourse('jsonToParse')

        def unpack(courseJson, decoded):
            decoded.name = courseJson['name']
            decoded.relatedCourses = courseJson['relatedCourses']
            decoded.reviews = pd.read_json(
                courseJson['reviews'], orient='split')
            decoded.institution = courseJson['institution']
            decoded.provider = courseJson['provider']
            decoded.attributes = courseJson['attributes']
            decoded.url = courseJson['url']
            decoded.numAdditionalInfo = courseJson['numAdditionalInfo']
            return decoded
        with open(Json) as courseJson:
            data = courseJson.read()
            data = json.loads(data)
            decoded = unpack(data, decoded)
        return decoded


def test():
    testCourse = classCentralCourse('test')
    testCourse.setUrl(
        'https://www.class-central.com/course/coursera-cloud-computing-concepts-part-1-2717?start=0')
    testCourse.updateReviews()
    encoder = classCentralEncoder()
    testEncodedJson = encoder.encode(testCourse)
    print('json works!')
    decoder = classCentralDecoder()
    decodedCourse = decoder.decodeJson('test.json')
    print('this works:', isinstance(decodedCourse, classCentralCourse))

test()
