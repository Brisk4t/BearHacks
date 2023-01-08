import json, re

# Adds courses that user took into a list
def get_courses(txt):
    courseList = txt.split(",")
    return courseList

import json

def can_take_course(user_courses, course_code, course_data):
  # Check if the course exists in the course data
  if course_code not in course_data:
    return False

  # Get the prerequisites for the course
  prerequisites = course_data[course_code]["course_prerequisites"]

  # If no prerequisites, the user can take the course
  if not prerequisites:
    return True

  # Split the prerequisites by ":" and "," to get a list of individual prerequisites
  prerequisites = prerequisites.split(":")[1].split(",")
  # Trim leading and trailing white space from the prerequisites
  prerequisites = [prereq.strip() for prereq in prerequisites]

  # Split the prerequisites by "or"
  prereq_groups = []
  for prereq in prerequisites:
    prereq_groups.extend(prereq.split("or"))
  # Trim leading and trailing white space from the prerequisites
  prereq_groups = [[p.strip() for p in group] for group in prereq_groups]

  # Check if the user has completed any of the prerequisites in each group
  for prereq_group in prereq_groups:
    if any(p in user_courses for p in prereq_group):
      continue
    else:
      return False
  # If the user has completed all of the prerequisites, they can take the course
  return True

# Example usage

# Load the course data from a JSON file
with open("courses.json") as f:
  course_data = json.load(f)

user_courses = ["AFNS401", "AFNS416"]
print(can_take_course(user_courses, "AFNS414", course_data))  # False
print(can_take_course(user_courses, "AFNS401", course_data))  # True

