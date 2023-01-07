import json
import re

def open_json():
    with open('ualberta_data/courses.json') as f:
        data = json.load(f)
    
    return data

def create_prerequisite(json_data):
    for course in json_data:
        if 'CMPUT' in course:
            prereq_string = json_data[course]['course_prerequisites']
            if prereq_string:
                if(prereq_string.partition('Corequisites:')[2]):
                    print(course + ":", end="")
                    print(prereq_string.partition('Corequisites:')[2])
                elif(prereq_string.partition('Corequisite:')[2]):
                    print(course + ":", end="")
                    print(prereq_string.partition('Corequisite:')[2])
                


def main():
    json_data = open_json() # Json_data -> Dict

    create_prerequisite(json_data)

    # print("CMPUT 174: ")
    # print(json_data["CMPUT267"]['course_prerequisites'])


main()