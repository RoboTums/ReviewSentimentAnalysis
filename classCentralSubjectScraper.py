import requests
from urllib.request import urlopen as uReq 
import urllib.error 
from bs4 import BeautifulSoup as soup
import pandas as pd
import re # regex
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from classCentralCourse import classCentralCourse
class classCentralSubjectScraper:
	def __init__(self,url,CourseListOfSubjects=None,urlList=None):
		self.url = url
		self.urlList=[]
		self.CourseListOfSubjects= []
	def getUrlList(self):
		return self.urlList
	def setUrlList(self,newList):
		self.urlList = newList
		return
	def appendToCourseList(self,courseObject):
		self.CourseListOfSubjects.append(courseObject)
		return
	def getListofCourseObj(self):
		return self.CourseListOfSubjects
	def setListofCourseObj(self,newList):
		self.CourseListOfSubjects = newList
		return

	def getCourseUrls(self):
		driver = webdriver.Firefox()
		driver.get(self.url)
		#click the button!!!
		try:
			while driver.find_element_by_id('show-more-courses')!= None:
				driver.find_elements_by_id('show-more-courses')[0].click()
		except ElementNotInteractableException:
			pass
		allCourseWebElements = driver.find_elements_by_xpath('//a[@class="text--charcoal text-2 medium-up-text-1 block course-name"]')  
		allSubjectUrl = [allCourseWebElements[i].get_attribute('href') for i in range(len(allCourseWebElements))]
		self.setUrlList(allSubjectUrl)
		driver.close()
		return allSubjectUrl
	def createSubjectDict(self):
		courseUrl= self.getUrlList()
		for i in range(len(courseUrl)):
			courseObj = classCentralCourse(str(i))
			courseObj.setUrl(courseUrl[i])
			courseObj.updateReviews()
			self.appendToCourseList(courseObj)
			#courseUrl.append(courseObj)
			#self.setListofCourseObj(courseUrl)
		return
