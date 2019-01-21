"""
@author: Daniel Firebanks
@usage:
    $ course_url = "https://www.coursera.org/learn/machine-learning"
    $ course = Course()
    $ course.get_reviews(10)
    $ course.build_reviews_df()
    $ course.export_reviews_df(file_path)
    $ course.build_course_json(optional_file_path)
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

class CourseraCourse:

    def __init__(self, url):
        """Only requires the URL of the ORIGINAL COURSE PAGE, the rest gets taken care of automatically"""

        self.url = url
        self.revs_url = self.url + "/reviews"
        #self.course_name = self.url.split("/")[-1]
        #print("Course Name:", self.course_name)

        self.driver = webdriver.Chrome("/Users/dafirebanks/chromedriver")  # Write the path of your own driver
        self.driver.get(self.revs_url)

        cname, cscore, cabout, cinst, cratings, crevs = get_other_attrs(self.driver)

        self.name = cname
        self.score = cscore
        self.description = cabout
        self.institution = cinst
        self.total_ratings = cratings

        # Total reviews that the course has
        self.total_reviews = crevs

        # {Number of stars: List of all reviews with those stars}
        self.reviews_dict = dict()
        self.all_reviews = []

        # Number of reviews we have
        self.num_reviews = 0

        self.df = None
        self.json = None

    def add_reviews(self, reviews):
        """Takes in a list of reviews, stores all of them and updates the review dictionary for the course"""
        self.all_reviews.extend(reviews)  # Make sure these aren't repeated
        
        for review in reviews:
            if str(review.stars) not in self.reviews_dict:
                self.reviews_dict[str(review.stars)] = [review]
            else:
                self.reviews_dict[str(review.stars)].append(review)

            self.num_reviews += 1
    
    def get_info(self):
        """Return course information"""
        return self.__str__()
    
    def __str__(self):
        return f"Name: {self.name} \
        \nScore: {self.score} \
        \nInstitution: {self.institution} \
        \nDescription: '{self.description}' \
        \nTotal Ratings: {self.total_ratings} \
        \nTotal Reviews: {self.total_reviews} \
        \nNumber of Reviews Extracted: {self.num_reviews} \n"

    def get_reviews(self, num_pages=10):
        """Extracts num_pages of results from course"""
        c_allrevs = []
        print("Starting to get reviews...")
        
        # Check if there are reviews first
        no_reviews_path = "//*[@id='root']/div[1]/div/div[3]/div[2]/p/span"
        if self.driver.find_elements_by_xpath(no_reviews_path):
            print(f"{self.name} by {self.institution} has no reviews!")
        else:
            # Get the first page of reviews
            c_allrevs.extend(extract_reviews(self.driver.page_source))
            pnum = 1

            # Get all the rest
            for i in range(num_pages):
                pnum += 1
                c_allrevs.extend(extract_reviews(click_next_page(self.driver, pnum)))

            self.add_reviews(c_allrevs)

    def has_reviews(self):
        if len(self.all_reviews) != 0:
            return True
        print("No reviews found!")
        return False

    def print_some_reviews(self, num):
        """Prints num reviews"""
        if self.has_reviews():
            for i in range(num):
                print(self.all_reviews[i])

    def build_reviews_df(self):
        """Builds pandas dataframe of reviews given review objects"""
        columns = ["Review Text", "Number of Stars", "Date of Review"]
        self.df = pd.DataFrame(columns=columns, index=(range(self.num_reviews)))

        if self.has_reviews()
            for i in range(self.num_reviews):
                rev = self.all_reviews[i]
                series = pd.Series([rev.text, rev.stars, rev.date])
                self.df.iloc[i, :] = series.values

    def export_reviews_df(self, file_path):
        """Converts pandas dataframe to csv and stores it in specified path"""
        if self.has_reviews():
            self.df.to_csv(file_path + self.name + "-" + self.institution + "-reviews.csv")

    def build_course_json(self, file_path=None):
        """Builds a JSON object containing all CourseraCourse attributes, and stores it in a json file if given file_path"""
        data = {"Name": self.name, "Institution": self.institution, "Score": self.score, "URL": self.url,
                "Reviews URL": self.revs_url, "All Reviews": self.df.to_json(), "Reviews by category": self.reviews_dict,
                "Number of reviews we have": self.num_reviews, "Total number of reviews on page": self.total_reviews,
                "Total number of ratings on page": self.total_ratings}

        if file_path:
            with open(file_path + self.name + "-" + self.institution + "json-obj.json") as outfile:
                json.dump(data, outfile)
        else:
            self.json = json.dumps(data)


class Review:
    def __init__(self, stars, text, date):
        self.stars = stars
        self.text = text
        self.date = date
    
    def __str__(self):
        return f"Number of Stars: {self.stars} \
        \nDate of Review: {self.date} \
        \nText of Review: '{self.text}'\n"


""" HELPER DRIVER FUNCTIONS BELOW!!!!!!!"""


def extract_reviews(page_link):
    """Given a reviews page link, it extracts all the reviews on that single result page"""
    soup = BeautifulSoup(page_link, "lxml")

    # Get the wrapper of all the the reviews from that page
    results = list(soup.find_all("div", attrs={"class": "review"}))

    # Iterate through results in one page and create list of review objects
    review_list = []

    for result in results:
        rev_wrap = result.contents[0]
        rev_text = rev_wrap.find_all("div", attrs={"class": "reviewText"})[0].text
        rev_date = rev_wrap.find_all("p", attrs={"class": "dateOfReview"})[0].text

        rev_stars_wrap = rev_wrap.find_all("label")
        rev_stars = 0
        for tag in rev_stars_wrap:
            if "Filled Star" in tag.text:
                rev_stars += 1

        review_list.append(Review(rev_stars, rev_text, rev_date))

    return review_list


def get_other_attrs(driver):
    """Gets all attributes of a course, given a driver with an opened page link"""
    about, score, name, inst, total_revs, total_ratings = None, None, None, None, None, None

    print("Getting other attributes...")

    try:
        about = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[2]/div/div/span[1]/span[1]").text
        score = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/span").text
        name_inst = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/h2").text.split(",")
        name, inst = name_inst[0], name_inst[1]
        total_revs = \
            driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/div[3]/div[2]/span").text.split(" ")[
                0]
        total_ratings = \
            driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/div[2]/span").text.split(" ")[0]

        print("Success in getting other attributes!")

    except Exception as e:
        print("Some attribute is missing!!!")
        print("Exception:", e)

    return about, score, name, inst, total_revs, total_ratings


def click_next_page(driver, page_num):
    """Click the next page of results, return resulting html"""
    button_path = "//*[@id='root']/div[1]/div/div[4]/nav/ul/li[13]/button"
    driver.find_element_by_xpath(button_path).click()
    print(f"Loading page {page_num}...")

    # Wait until the results load, this should be adjusted depending on the internet speed
    try:
        WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH,
                                                                          "//*[@id='root']/div[1]/div/div[4]/div[2]/p/span")))
        print("Got it!")
        print()
        return driver.page_source

    except:
        print(f"Result page {page_num} did not load, moving on to the next one...")
        click_next_page(driver, page_num=page_num+1)
