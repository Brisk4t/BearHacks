import json
import os
import openai

openai.api_key = "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"


def open_json():
    with open('ualberta_data/courses.json') as f:
        data = json.load(f)
    
    return data


def write_json(data):
    with open("ualberta_data/courses.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def prereq_prompt(prereq_body):
    get_prerequisites = "Find the number of prerequisites for this course:" + prereq_body

    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=get_prerequisites,
    temperature=0.7,
    max_tokens=709,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    print(response.choices[0].text)


def create_prerequisite(json_data):
    for course in json_data:
        if 'CMPUT' in course:
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

                

    write_json(json_data)
                

def main():
    json_data = open_json() # Json_data -> Dict

    with open('courses.txt', 'w') as f:
        for course in json_data:
            f.write(course)
            f.write('\n')


    
    #create_prerequisite(json_data)

    #prereq_prompt(json_data['CMPUT267']['course_prerequisites'])

    # print("CMPUT 174: ")
    # print(json_data["CMPUT267"]['course_prerequisites'])


main()