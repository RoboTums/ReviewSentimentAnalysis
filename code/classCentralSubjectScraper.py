import requests
from urllib.request import urlopen as uReq
import urllib.error
from bs4 import BeautifulSoup as soup
import pandas as pd
import re  # regex
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from classCentralCourse import classCentralCourse
from classCenJson import classCentralEncoder, classCentralDecoder
import os.path
import json
class classCentralSubjectScraper:
    def __init__(self, url, CourseListOfSubjects=None, urlList=None):
        self.url = url
        self.urlList = []
        self.subjectUrlList = ['https://www.class-central.com/subject/cs', 'https://www.class-central.com/subject/business', 'https://www.class-central.com/subject/data-science',
                              'https://www.class-central.com/subject/programming-and-software-development', 'https://www.class-central.com/subject/maths']
        self.CourseListOfSubjects = []

    def getUrlList(self):
        return self.urlList

    def setUrlList(self, newList):
        self.urlList = newList
        return

    def appendToCourseList(self, courseObject):
        self.CourseListOfSubjects.append(courseObject)
        return

    def getListofCourseObj(self):
        return self.CourseListOfSubjects

    def setListofCourseObj(self, newList):
        self.CourseListOfSubjects = newList
        return
    def allCoursesToJson(self,fileCreate=False):
    	courseList = self.getListofCourseObj()
    	#print('the course list:',courseList)
    	encoder = classCentralEncoder(fileCreation=False)
    	listToDump = [encoder.encode(course) for course in courseList]
    	if fileCreate:
    		with open('courseData.json','w') as file:
    			json.dump(listToDump,file)
    	return listToDump
    def allCoursesFromJson(self,jsonObj):	
    	decoder = classCentralDecoder()
    	print('json obj type : ',type(jsonObj))
    	#check to see if file or string
    	if os.path.isfile(str(jsonObj)):
    		decoded =decoder.decodeJsonFile(jsonObj)
    		allCourses = [decoder.decodeJsonString(course) for course in decoded]
    	else:
    		#decoded = decoder.decodeJsonString(jsonObj)
    		allCourses = [decoder.decodeJsonString(course) for course in jsonObj]
    	self.setListofCourseObj(allCourses)
    	return



    def exportListofCourseUrls(self):
        toExport = pd.DataFrame(self.getUrlList(), columns=['url'])
        toExport.to_csv('classCenCourseUrl.csv')
        return

    def getCourseUrls(self, url=None):
        driver = webdriver.Firefox()
        if url == None:
            driver.get(self.url)
        else:
            driver.get(url)
        try:
            while driver.find_element_by_id(
                    'show-more-courses') is not None:
            	#if driver.find_element_by_class_name('text-center padding-vert-medium')
 
                driver.find_elements_by_id('show-more-courses')[0].click()
        except ElementNotInteractableException:
            pass
        except ElementClickInterceptedException:
        	print('popup closed')
        	driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button').click()
        allCourseWebElements = driver.find_elements_by_xpath(
            '//a[@class="text--charcoal text-2 medium-up-text-1 block course-name"]')
        allSubjectUrl = [allCourseWebElements[i].get_attribute(
            'href') for i in range(len(allCourseWebElements))]
        self.setUrlList(allSubjectUrl)
        driver.close()	
        return allSubjectUrl

    def createSubjectDict(self):
        courseUrl = self.getUrlList()	
        for i in range(len(courseUrl)):
            courseObj = classCentralCourse(str(i))
            courseObj.setUrl(courseUrl[i])
            courseObj.updateReviews()
            courseObj.grabDescriptors()
            self.appendToCourseList(courseObj)
        return

    def scrapeAllUrlLocations(self):
        urlLoc = self.subjectUrlList
        massUrl = []	
        for subj in range(len(urlLoc)):
            massUrl.extend(self.getCourseUrls(urlLoc[subj]))
        panUrl = pd.Series(massUrl, index=range(len(massUrl))).unique().tolist()        # remove duplicates
        self.setUrlList(panUrl)
        return	
