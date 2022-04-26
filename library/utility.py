import json
import time

# Contains function for utility.
def replace_str_word(string, word, replace):
    for i in range(len(string) - len(word) + 1):
        if string[i: i + len(word)] == word:
            crit_i = i
            break
    
    str_former = string[0: crit_i]
    str_latter = string[crit_i + len(word):]

    return str_former + replace + str_latter

# Necessarily convert all lists to tuples.
def get_tupled_list(still_list):
    if type(still_list) is list:
        for i in range(len(still_list)):
            if type(still_list[i]) is list:
                still_list[i] = tuple(still_list[i])
        return tuple(still_list)
    else:
        return still_list

# Get data from the json file.
def get_json_data(path):
    with open(path, encoding='utf-8', mode='r') as data_json:
        data = json.loads(data_json.read())
    
    return data

# Special seating according to weeks passed.
def get_pair_by_week(name_list):
    week_coord = time.time() // (86400 * 7)
    get_index = int(week_coord % len(name_list))
    
    if get_index < len(name_list) - 1:
        return tuple(name_list[get_index: get_index + 2])
    else:
        return (name_list[-1], name_list[0])