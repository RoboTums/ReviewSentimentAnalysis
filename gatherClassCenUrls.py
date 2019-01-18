from classCentralCourse import 	classCentralCourse
from classCentralSubjectScraper import classCentralSubjectScraper


def main():
	queen = classCentralSubjectScraper('Niadra')
	queen.scrapeAllUrlLocations()
	queen.createSubjectDict()
	jsonList = queen.allCoursesToJson(fileCreation=True)
	print(jsonList)
	queen.allCoursesFromJson(jsonList)
	print(queen.getListofCourseObj())
	#queen.exportListofCourseUrls()
main()