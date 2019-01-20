from CourseraClass import Course

def main():
    course_url = "https://www.coursera.org/learn/machine-learning"
    course = Course(course_url)
    course.get_reviews(10)
    course.build_df()
    course.export_df()

main()

