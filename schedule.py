from bearhacks import *
import random
from itertools import combinations

def build_degree(json_data, degree_data):
    degree = []
    
    
    # for year in degree_data:
    #     print(year)

    #print(degree_data["year4"])
    
    optional = random.sample(degree_data["year4"]["courses"][0]["courses"], degree_data["year4"]["courses"][0]["choose"])
    chosen = []

    for item in optional:
        chosen.append(item["name"])

    optional = []
    for i in json_data:
        if "CMPUT 4" in i:
            optional.append(i)
    
    opt2 = (random.sample(optional, degree_data["year4"]["courses"][1]["choose"]))

    for item in opt2:
        chosen.append(item)

    avg_diff = 0
    for item in chosen:
        avg_diff = avg_diff + json_data[item]["difficulty"]

    all_difficulties = []

    
    random_choices = random.sample(sorted(json_data), 100)
    
    for item in random_choices:
        all_difficulties.append(json_data[item]["difficulty"])

    

    # for item in json_data:
    #     if (len(all_difficulties) < 100):
    #         if not item in chosen:
    #             if random.randint(0,1):
    #                 all_difficulties.append(json_data[item]["difficulty"])

    all_difficulties.sort()

    diff_list = pick_numbers(all_difficulties, 4, avg_diff)


    for item in json_data:
        if json_data[item]["difficulty"] in diff_list:
                chosen.append(item)


    for item in (random.sample(chosen, 5)):
        degree.insert(0, item)
        chosen.remove(item)

    for item in (random.sample(chosen, 5)):
        degree.insert(0, item)
        chosen.remove(item)
    

    for item in degree:
        fill_preq(item, degree, json_data)


    return degree



def fill_preq(course, degree, json_data):
    
    for item in degree:
        if(len(degree) < 40):
            preqs = get_courses(json_data[item]["course_prerequisites"])
            for item in preqs:
                degree.insert(0, random.choice(item))


def pick_numbers(numbers, n, target):
  # Get all combinations of `n` numbers from `numbers`
  combs = list(combinations(numbers, n))
  
  # Find the combination that has a sum closest to `target`
  closest_comb = min(combs, key=lambda x: abs(sum(x)-target))
  
  return closest_comb

