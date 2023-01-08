import json, re
from bearhacks import *

# Adds courses that user took into a list
def getUserCourses(txt):
    courseList = txt.split(",")
    return courseList

def can_take_course(user_courses, course_code, course_data):
  # Check if the course exists in the course data
  if course_code not in course_data:
    return False

  # Get the prerequisites for the course
  prerequisites = get_courses(course_data[course_code]['course_prerequisites'])


  # If no prerequisites, the user can take the course
  if not prerequisites:
    return True


 
  # Trim leading and trailing white space from the prerequisites
  #prereq_groups = [[p.strip() for p in group] for group in prereq_groups]

  # Check if the user has completed any of the prerequisites in each group
  for prereq_group in prerequisites:
    if any(p in user_courses for p in prereq_group):
      continue
    else:
      return False
  # If the user has completed all of the prerequisites, they can take the course
  return True


# Load the course data from a JSON file
courseData =  open_json("ualberta_data/courses.json") # Json_data -> Dict

user_courses = ["CMPUT 174", "CMPUT 175"]
print("--------------------------------------------")
print(can_take_course(user_courses, "CMPUT 201", courseData))  
print(can_take_course(user_courses, "CMPUT 272", courseData))  
print("--------------------------------------------")
