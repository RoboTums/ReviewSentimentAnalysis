"""
@author: Daniel Firebanks
@usage: Example application of CourseraClass, basically a test
"""
from CourseraClass import CourseraCourse


def main():
    course_url = "https://www.coursera.org/learn/python-data-analysis"
    course = CourseraCourse(course_url)
    course.get_info()
    course.get_reviews(10)

    # Check if there are reviews first
    if len(course.all_reviews) != 0:
        course.print_some_reviews(20)
        course.build_df()
        course.export_df(file_path="/Users/dafirebanks/Documents/") # Works all the way till here!


main()
