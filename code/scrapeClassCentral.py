from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup
import pandas as pd
import re # regex

#Make columns in the column list for dataframe later
columns = ['reviewText','reviewRating','completionStatus','hoursWeekly','difficulty']#refactor to read in the csv headers so we dont have to do this every time
difficultyText = ['very easy','easy','medium','hard','very hard']
#open connection. Replace with master list of webURLS
my_url ='https://www.class-central.com/course/coursera-learning-how-to-learn-powerful-mental-tools-to-help-you-master-tough-subjects-2161'

uClient= uReq(my_url)
page_html = uClient.read()
uClient.close()

#html
page_soup=soup(page_html,"html.parser")
#grabs all first reviews
containers = page_soup.findAll('div',{'id':"reviews-items"})

#create list of reviews
reviews = containers[0].findAll('div',{'class':'border-all border--gray-xlight radius padding-large single-review margin-top-medium margin-bottom-large'})
num_reviews = range(len(reviews)) # to iterate, also index.
reviewData = pd.DataFrame(columns=columns, index=num_reviews)

# for each review, grab feedback and text
feedBackMaster = []
for i in num_reviews:
	feedBackMaster.append(reviews[i].findAll('div',{'class':'review-title title-with-image margin-top-xsmall text-2'})[0].text)  
	
#strip all
feedBackMaster = [feedBackMaster[i].strip().strip('.') for i in range(len(feedBackMaster))] 
#review-title title-with-image margin-top-xsmall text-2
#process review
for i in num_reviews:
	progressStatus = feedBackMaster[i].find('completed')
	#progress status will be -1 if not found, so we add 1 so zero represents an incomplete course
	progressStatus+=1
	reviewData.iloc[i].completionStatus = progressStatus
	additionalInfo = feedBackMaster[i].find('spending')
	#if there is addtional info
	if additionalInfo != -1:
		#find hours spent weekly
		hoursSpent = [(inte,pos) for inte, pos in enumerate(reviewFeedbaq[8]) if pos.isdigit()]
		hoursSpent = int(hoursSpent[0][1])
		reviewData.iloc[i].hoursWeekly = hoursSpent
		#find reported difficulty
		difficulty = [re.search(i,reviewFeedbaq[8]) == None  for i in difficultyText]
		difficulty = [i for i in range(len(result)) if result[i]==False][0] 
		reviewData.iloc[i].difficulty = difficulty
reviewData
