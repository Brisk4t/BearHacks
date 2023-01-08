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
  if not prerequisites :
    return True


 
  #prereq_groups = [[p.strip() for p in group] for group in prereq_groups]

  # Check if the user has completed any of the prerequisites in each group
  for prereq_group in prerequisites:
    if any(p in user_courses for p in prereq_group):
      continue
    else:
      return False
  # If the user has completed all of the prerequisites, they can take the course
  return True

def course_names(course_data):
    return list(course_data.keys())


def create_schedule(user_courses, catalouge_data, course_data):
  # Load the JSON file and parse the data
  

  # Get the required and optional courses
  # This is year 1, depedning on the year of study we can add a for loop.
  required_courses = catalouge_data["year1"]["required courses"]
  optional_courses = catalouge_data["year1"]["optional courses"]["courses"]
  print("-------------------------------------------")
  print(optional_courses)

  # Filter the required courses to only include those that the user is eligible to take
  eligible_required_courses = [c for c in required_courses if can_take_course(user_courses, c["name"], course_data)]

  # Create a list of eligible optional courses
  eligible_optional_courses = []
  for set_ in optional_courses:
    courses = set_["courses"]
    if set_["name"] == "optional courses":
      # Add all optional courses
      eligible_optional_courses.extend(courses)
    else:
      # Filter the courses in the set to only include those that the user is eligible to take
      for c in courses:
        print("XXXXXXXXXXXXXXXXXX")
        print(c)
        print("XXXXXXXXXXXXXXXXXX")
      eligible_optional_courses.extend([c for c in courses if can_take_course(user_courses, c["name"], course_data)])

  # Choose the required number of courses from each set of optional courses
  chosen_optional_courses = []
  for set_ in optional_courses:
    choose = set_["choose"]
    courses = set_["courses"]
    chosen_courses = []
    for i in range(choose):
      # Let the user choose a course from the set
      print(f"Choose a course from {set_['name']}:")
      for j, c in enumerate(courses):
        print(f"{j + 1}: {c['name']} - {c['title']}")
      choice = int(input("Enter the number of course"))
      chosen_courses.append(courses[choice - 1])
      # Remove the chosen course from the list of eligible optional courses
      eligible_optional_courses.remove(courses[choice - 1])
    chosen_optional_courses.extend(chosen_courses)
  schedule = eligible_required_courses + chosen_optional_courses

  return schedule





def main():
  # Load the course data from a JSON file
  courseData =  open_json("ualberta_data/courses.json") # Json_data -> Dict
  catalouge_data = open_json("ualberta_data/CMPUTcatalouge.json")
  courseCodeList = course_names(course_data=courseData)
  print(courseCodeList)
  user_courses = ["CMPUT 174", "CMPUT 175", "CMPUT 272","CMPUT 201"]
  print("--------------------------------------------")
  print(can_take_course(user_courses, "CMPUT 201", courseData))  
  print(can_take_course(user_courses, "CMPUT 272", courseData))  
  print(can_take_course(user_courses, "CMPUT 291", courseData))  

  print("--------------------------------------------")
  sch = create_schedule(user_courses,catalouge_data,courseData)
  print(sch)

main() 