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
    def __init__(self, fileCreation=True):
        super().__init__()
        self.fileCreation = fileCreation
    def default(self, course):

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
                'numAdditionalInfo': course.numAdditionalInfo
            }
            if self.fileCreation:
                with open(filename, 'w') as outfile:
                   json.dump(jsonReady, outfile)
                   
            return jsonReady
        else:
            super().default(self, course)


# decodes course from json
class classCentralDecoder:
        # takes in json file name
    def unpack(self,courseJson, decoded):
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
    def decodeJsonString(self,JsonString):
        decoded = classCentralCourse('jsonToParse')
        #print(repr(JsonString))
        data = json.loads(JsonString)
        
        decoded = self.unpack(data,decoded)
        return decoded
    def decodeJsonFile(self,Json):
        decoded = classCentralCourse('jsonToParse')
        
        with open(Json) as courseJson:
            data = courseJson.read()
            #print('data type is ', type(data))
            data = json.loads(data)
            decoded = self.unpack(data, decoded)
        return decoded


def testOne():
    testCourse = classCentralCourse('test')
    testCourse.setUrl(
        'https://www.class-central.com/course/coursera-cloud-computing-concepts-part-1-2717?start=0')
    testCourse.updateReviews()
    encoder = classCentralEncoder(True)
    testEncodedJson = encoder.encode(testCourse)
    decoder = classCentralDecoder()
    decodedCourse = decoder.decodeJsonFile('test.json')
    print('Test one works:', isinstance(decodedCourse, classCentralCourse))

def testTwo():
    testCourse = classCentralCourse('test')
    testCourse.setUrl(
        'https://www.class-central.com/course/coursera-cloud-computing-concepts-part-1-2717?start=0')
    testCourse.updateReviews()
    encoder = classCentralEncoder(fileCreation=False)
    testEncodedJson = encoder.encode(testCourse)
    #print('json works!', repr(testEncodedJson))
    decoder = classCentralDecoder().decodeJsonString(testEncodedJson)
    #decodedCourse = decoder
    print('Test two works:', isinstance(decoder, classCentralCourse))

#testOne()
#testTwo()
