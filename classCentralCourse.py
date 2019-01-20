# course class to scrape class central courses with.

# all you need to do is specify a url and grab the reviews

# Usage: trial = classCentralCourse('named!')
# trial.setUrl('https://www.class-central.com/course/kadenze-creative-applications-of-deep-learning-with-tensorflow-6679')
# trial.updateReviews()
# trial.getReviews() <- returns a dataframe of that courses reviews.
# further things coming soon
import requests
from urllib.request import urlopen as uReq
import urllib.error
from bs4 import BeautifulSoup as soup
import pandas as pd
import re  # regex
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException


class classCentralCourse:
	def __init__(self, name, relatedCourses=None, description=None, reviews=None,
				 provider=None, attributes=None, url=None, institution=None, numAdditionalInfo=0):
		# a bunch of instance vars lol
		self.name = name
		self.relatedCourses = relatedCourses
		self.description = description
		self.reviews = reviews
		self.institution = institution
		self.provider = provider
		self.attributes = attributes
		self.url = url

		# added this later on, its the number of people who added additonal
		# info on their website.
		self.numAdditionalInfo = numAdditionalInfo

	# getters and setters
	def getNumAdditionalInfo(self):
		return self.numAdditionalInfo

	def getName(self):
		return self.name

	def getRelatedCourses(self):
		return self.relatedCourses

	def getDescription(self):
		return self.description

	def getReviews(self):
		return self.reviews

	def getCourseProvider(self):
		return self.provider

	def getAttrs(self):
		return self.attributes

	def getUrl(self):
		return self.url

	def setName(self, newName):
		self.name = newName
		return

	def setNumAdditionalInfo(self, newnumAdditionalInfo):
		self.numAdditionalInfo = newnumAdditionalInfo
		return

	def setRelatedCourses(self, newRelatedCourses):
		self.relatedCourses = newRelatedCourses
		return

	def setDescription(self, newDescript):
		self.description = newDescript
		return

	def setReviews(self, newReviews):
		self.reviews = newReviews
		return

	def setInstitution(self, newinstitution):
		self.institution = newinstitution
		return

	def setProvider(self, newprovider):
		self.provider = newprovider
		return

	def setAttrs(self, newAttrs):
		self.attributes = newAttrs
		return

	def setUrl(self, newUrl):
		self.url = newUrl
		return

	def grabHTML(self, url):
		uClient = uReq(url)
		page_html = uClient.read()
		uClient.close()
		html = soup(page_html, 'html.parser')
#        except urllib.URLError:
#            html = None
#            print("URLError: ",url)
#        except urllib.gaierror:
#            html = None
#            print('bad link: ', url)

		return html

	def getReviewText(self, review):
		review = review.findAll(
			'div', {'class': 'review-content text-2 margin-vert-small'})
		return review[0].text.strip()

	def getRating(self, review):
		review = review.findAll(
			'span', {
				'class': 'review-rating medium-up-hidden text--charcoal'})
		return review[0].text.strip()

	def getStatus(self, review):
		review = review.findAll('span',
								{'class': 'text--italic'})[0].text.strip()
		if review == 'completed this course.':
			return 1
		else:
			# theres additonal info
			self / setNumAdditionalInfo((getNumAdditionalInfo() + 1))
			return 0

	def formBaseUrl(self, url):
		return url + "?start="

	def editUrl(self, url, step):
		url = self.formBaseUrl(self.getUrl())
		url = url + str(step)
		return url

	def getAdditionalInfo(self, containers):
		containers = containers.findAll('div', {'id': 'reviews-items'})

		rows = containers[0].findAll(
			'div', {'class': 'review-title title-with-image margin-top-xsmall text-2'})
		difficultyText = [
			'very easy',
			'easy',
			'medium',
			'hard',
			'very hard']

		output = []
		for i in range(len(rows)):
			rowInfo = []
			if 'completed this course' in rows[i].text.strip():
				rowInfo.append(1)
			else:
				rowInfo.append(0)
			if 'spending' in rows[i].text.strip():
				# get hours
				hours = int([(inte, pos) for inte, pos in enumerate(
					rows[i].text.strip()) if pos.isdigit()][0][1])
				rowInfo.append(hours)
				# get difficulty
				dif = [re.search(j, rows[i].text.strip())
					   is None for j in difficultyText]
				rowData = [j for j in range(len(dif)) if dif[j] == False]
				if rowData:
					rowInfo.append(rowData[0])
				else:
					rowInfo.append(None)
			else:
				rowInfo.extend([None, None])
			if True:
				output.append(rowInfo)
		return output
	def grabDescriptors(self):
		# first we grab the description
		scraper = webdriver.Firefox()
		try:
			scraper.get(self.getUrl())
			descriptionELement = scraper.find_elements_by_xpath('/html/body/div[1]/div[1]/div[4]/div/div[3]/section[1]/div[2]/article/div')
			description = descriptionELement[0].text 
			self.setDescription(description)

			# then we can grab other items (like institution)
			institution = scraper.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div/div[1]/div/p/a[1]').text
			self.setInstitution(institution)
			#get provider
			provider  = scraper.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div/div[1]/div/p/a[2]').text
			self.setProvider(provider)
			#get tags/ attributes
			tags =  scraper.find_elements_by_xpath('/html/body/div[1]/div[1]/div[4]/div/div[3]/section[1]/div[3]/div/a')
			attributes = [tag.text for tag in tags]
			self.setAttrs(attributes)
			#get related courses
			related = scraper.find_elements_by_xpath('')
			scraper.close()
		except ElementClickInterceptedException:
			print('popup closed')
			driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button').click()
		return 
	def reviewFilter(self, soup):  # returns a list of reviews
		# print(soup)
		soup = soup.findAll('div', {'id': 'reviews-items'})
		if not soup:
			return []
		else:
			reviewList = soup[0].findAll(
				'div', {
					'class': 'border-all border--gray-xlight radius padding-large single-review margin-top-medium margin-bottom-large'})
			return reviewList

	def getNumberOfReviews(self, soup):
		x = soup.findAll('a', {'id': 'read-reviews'})
		x = x[0].findAll(
			'span', {
				'class': 'text--underline inline-block padding-right-xxsmall'})
		x = int(re.findall(r'\d+', x[0].text.strip())[0])
		return x
	   # (re.findall('\d+', str1 ))

	def processReviews(self, listReviewSoup, reviewDF, page_soup):
		reviewDF = pd.DataFrame(index=reviewDF.index, columns=reviewDF.columns)
		for idx in range(len(listReviewSoup)):
			review = listReviewSoup[idx]
			additionalInfo = self.getAdditionalInfo(page_soup)
			# make dataframe to append

			appender = pd.Series([self.getReviewText(review), self.getRating(review), additionalInfo[idx][0], additionalInfo[idx][2], additionalInfo[idx][1]],
								 index=[reviewDF.columns])
			# print(appender.shape)
			reviewDF.iloc[idx, :] = appender.values
		self.setReviews(reviewDF)
		return reviewDF

	def updateReviews(self):
		# refactor to read in the csv headers so we dont have to do this every
		# time
		columns = [
			'reviewText',
			'reviewRating',
			'completionStatus',
			'hoursWeekly',
			'difficulty']

		page_soup = self.grabHTML(self.getUrl())
		# sanity check
		# print(page_soup)
		numReviews = range(self.getNumberOfReviews(page_soup))
		# sanity check:  print(numReviews)
		reviewDF = pd.DataFrame(columns=columns, index=(numReviews))
		revHTML = self.reviewFilter(page_soup)

		if len(numReviews) > 20:
			#url = self.formBaseUrl(self.getUrl())+str('0')
			extensions = [i for i in numReviews if i % 20 == 0]
			# print(extensions)
			multiDataFrames = []
			for rev in extensions:
				url = self.editUrl(self.getUrl(), rev)

				print(url)
				html = self.grabHTML(url)
				review = self.reviewFilter(html)
				df = self.processReviews(review, reviewDF, page_soup)
				# print(df)

				multiDataFrames.append(df)
				if len(multiDataFrames) > 1:
					multiDataFrames = [
						multiDataFrames[0].append(
							multiDataFrames[1])]
					# print(multiDataFrames)
			almost = multiDataFrames[0]
			done = almost.dropna(subset=['reviewText'])
			done.index = range(len(done['reviewText']))
			self.setReviews(done)
		else:
			self.processReviews(revHTML, reviewDF, page_soup)
		# now to get specific columns
