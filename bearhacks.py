import json
import os
import openai
import re
import random

# openai.api_key = "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"


def open_json(json_location):
    absolute_path = os.path.dirname(__file__)
    relative_path = json_location
    full_path = os.path.join(absolute_path, relative_path)
    with open(full_path) as f:
        data = json.load(f)
    
    return data


def write_json(data, json_location):
    absolute_path = os.path.dirname(__file__)
    relative_path = json_location
    full_path = os.path.join(absolute_path, relative_path)

    with open(full_path, "w") as jsonFile:
        json.dump(data, jsonFile)


# def prereq_prompt(prereq_body):
#     get_prerequisites = "Find the number of prerequisites for this course, ignore consent of the instructor :" + prereq_body

#     response = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt=get_prerequisites,
#     max_tokens=1024,
#     n=4,
#     stop=None,
#     temperature=0.5,
# )

#     print(response.choices[2].text)


def create_prerequisite(json_data):
    for course in json_data:
            prereq_string = json_data[course]['course_prerequisites']
            if prereq_string:
                if(prereq_string.partition('Corequisites:')[2]):
                    print(course + ":", end="")
                    json_data[course]['course_corequisites'] = prereq_string.partition('Corequisites:')[2];
                    json_data[course]['course_prerequisites'] = prereq_string.partition('Corequisites:')[0];
                    print(json_data[course]['course_corequisites'])

                elif(prereq_string.partition('Corequisite:')[2]):
                    print(course + ":", end="")
                    json_data[course]['course_corequisites'] = prereq_string.partition('Corequisite:')[2];
                    json_data[course]['course_prerequisites'] = prereq_string.partition('Corequisite:')[0];
                    print(json_data[course]['course_corequisites'])

                else:
                    json_data[course]['course_corequisites'] = None

                

    return json_data


def get_courses(s):
    courses = []

    # Split the string on the semicolon character
    for item in s.split(';'):
        
        code = re.findall("(and [A-Z]{3,5} \d{3}|or \d{3}|[A-Z]{3,5} \d{3}|, \d{3}| or [A-Z]{3,5} \d{3})", item) # retuns a list of XXXX YYY / or XXX / or , XXX
        
        
        alts = []
        alts2 = []
        
        for match in code:
            if("and" in match):
                
                alts2.append(match.partition('and ')[2])
                

            else:
                
                
                if(", " in match):
                    alts.append(alts[0].partition(" ")[0] + " " + match.partition(", ")[2])

                elif('or' in match):
                    part = match.partition('or ')[2]
                    if(len(part) == 3):
                        alts.append(alts[0].partition(" ")[0] + " " + part)

                    else:
                        alts.append(match.partition('or ')[2])
                
                else:
                    alts.append(match)

        if(alts):
            courses.append(alts)
        
        if(alts2):
            courses.append(alts2)
            

        #courses[code] = numbers

    return courses

def substisute_difficulty(json_data):
    for course in json_data:
        json_data[course]['difficulty'] = random.uniform(-1, 1)
    
    return json_data

def main():
    json_data = open_json("ualberta_data/courses.json") # Json_data -> Dict

    
    #json_data = create_prerequisite(json_data)
    #json_data = substisute_difficulty(json_data)
    #write_json(json_data, "ualberta_data/courses.json")

    print(json_data['CMPUT 272']['course_prerequisites'])
    print(get_courses(json_data['CMPUT 272']['course_prerequisites']))

    #prereq_prompt(json_data['CMPUT291']['course_prerequisites'])


main()