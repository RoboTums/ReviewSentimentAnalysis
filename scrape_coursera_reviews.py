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
    course.print_some_reviews(20)
    course.build_df()
    course.export_df(file_path="Insert_file_path_here!")
    course.build_json(file_path="Optional")  # Works all the way till here!

main()
