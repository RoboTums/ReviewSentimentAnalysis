from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup

#open connection
my_url ='https://www.class-central.com/course/coursera-learning-how-to-learn-powerful-mental-tools-to-help-you-master-tough-subjects-2161'

uClient= uReq(my_url)
page_html = uClient.read()
uClient.close()

#html
page_soup=soup(page_html,"html.parser")
#grabs all first reviews
containers = page_soup.findAll('div',{'id':"reviews-items"})
print(	(containers))