from CourseraClass import Course

def main():
    course_url = "https://www.coursera.org/learn/machine-learning"
    course = Course(course_url)
    course.get_reviews(10)
    course.build_df()
    course.export_df()

main()

#####################################################################################################################

# def click_next_page(driver, page_num):
#     """Click the next page of results, return resulting html"""
#     button_path = "//*[@id='root']/div[1]/div/div[4]/nav/ul/li[13]/button"
#     driver.find_element_by_xpath(button_path).click()
#     print(f"Loading page {page_num}...")
#
#     try:
#         WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div[1]/div/div[4]/div[2]/p/span"))) # Wait until the results load, this should be adjusted depending on the internet speed
#         print("Got it!")
#         print()
#
#     except:
#         print(f"Result page {page_num} did not load, moving on to the next one...")
#
#     return driver.page_source
#
# def extract_reviews(page_link):
#     soup = BeautifulSoup(page_link, "lxml")
#
#     # Get the wrapper of all the the reviews from that page
#     results = list(soup.find_all("div", attrs={"class":"review"}))
#
#     # Iterate through results in one page and create list of review objects
#     review_list = []
#
#     for result in results:
#         rev_wrap = result.contents[0]
#         rev_text = rev_wrap.find_all("div", attrs={"class":"reviewText"})[0].text
#         rev_date = rev_wrap.find_all("p", attrs={"class":"dateOfReview"})[0].text
#
#         rev_stars_wrap = rev_wrap.find_all("label")
#         rev_stars = 0
#         for tag in rev_stars_wrap:
#             if "Filled Star" in tag.text:
#                 rev_stars += 1
#
#         review_list.append(Review(rev_stars, rev_text, rev_date))
#
#     return review_list
#
# def get_other_attrs(driver):
#     about = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[2]/div/div/span[1]/span[1]").text
#     score = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/span").text
#     name_inst = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/h2").text.split(",")
#     name, inst = name_inst[0], name_inst[1]
#     total_revs = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/div[3]/div[2]/span").text.split(" ")[0]
#     total_ratings = driver.find_element_by_xpath("//*[@id='root']/div[1]/div/div[1]/div/div[2]/div[2]/span").text.split(" ")[0]
#
#     return about, score, name, inst, total_revs, total_ratings

# def main():
#     # Initialize driver
#     driver = webdriver.Chrome("/Users/dafirebanks/chromedriver")
#
#     # Access url
#     course_url = "https://www.coursera.org/learn/machine-learning"
#     revs_url = course_url + "/reviews"
#     driver.get(revs_url)
#
#     c_allrevs = []
#
#     # Get the first page of reviews
#     c_allrevs.extend(extract_reviews(driver.page_source))
#     pnum = 1
#
#     #Get all the rest
#     for i in range(10):
#         pnum += 1
#         c_allrevs.extend(extract_reviews(click_next_page(pnum)))
#
#     # Get other attributes of course
#     cname, cscore, cabout, cinst, cratings, crevs = get_other_attrs(driver)
#
#     # Initialize course object
#     course = Course(name=cname, score=cscore, description=cabout, institution=cinst, total_ratings=cratings, total_reviews=crevs, url=course_url)
#     course.add_reviews(c_allrevs)

