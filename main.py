import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import codecs, json
import unicodedata
import collections
import datetime
import math
import re
# pip install Unidecode  <OR> conda install Unidecode
import unidecode

#importing all csv files
domarar = pd.read_csv('csv/blak-domarar.csv', sep=';', header=0)
einstaklingar = pd.read_csv('csv/blak-einstaklingar.csv', sep=';', header=0)
forsvarsmenn = pd.read_csv('csv/blak-forsvarsmenn.csv', sep=';', header=0)
lid = pd.read_csv('csv/blak-lid.csv', sep=';', header=0)
lidimoti = pd.read_csv('csv/blak-lidimoti.csv', sep=';', header=0)
lidsmenn = pd.read_csv('csv/blak-lidsmenn.csv', sep=';', header=0)
lidsstjorar = pd.read_csv('csv/blak-lidsstjorar.csv', sep=';', header=0)
thjalfarar = pd.read_csv('csv/blak-thjalfarar.csv', sep=';', header=0)
mot = pd.read_csv('csv/blak-mot.csv', sep=';', header=0)

# drop all SyndarLids with an ID (SyndarlidID)
# (the reason for not dropping using SyndarLid is because I don't trust that column to be inserted correctly with [0,1])
lid = lid[lid['SyndarlidID'].isna()]
# then dropping those two columns because we don't want virtual teams
lid = lid.drop(columns=['SyndarLid', 'SyndarlidID'])
# all the Heimilisfang columns are empty so we can remove them
einstaklingar = einstaklingar.drop(columns=['Heimilisfang1', 'Heimilisfang2', 'Heimilisfang3'])

# All duplicated birthdays
duplicated_einstaklingar = einstaklingar[einstaklingar.duplicated(subset=['Nafn', 'Fdagur', 'Kyn'], keep=False)]
duplicated_fdagur_kyn_einstaklingar = einstaklingar[einstaklingar.duplicated(subset=['Fdagur', 'Kyn'], keep=False)]

# variable to be used
lidi = lid
duplicate_dict = defaultdict(dict)
dict_removed_single_entries = defaultdict(dict)
dict_name_entries = {}
duplicate_ids_kept = []
dict_duplicate_compare_team_members = defaultdict(dict)
dict_einstaklingar_teammember_info = {}
not_the_same_person = {}
most_likely_same_person = {}
merged_list = {}


def isaRadNumber(x):
    valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
    return x in valid


def correctRadNumbersFromEntries():
    for index, row in lidi.iterrows():
        radNumber = row['Radnumer']
        id = row['LidID']

        if(not(isaRadNumber(radNumber))):
            #print("needs to modify id ", id)
            name = row['Nafn']
            size = len(name.split())
            # club name is first part
            club = ' '.join(name.split()[:max(1, (size-2))])
            ordinal = name.split()[size-1]  # last str

            # if name ends with a single char, used for radnumbers
            if(len(ordinal) == 1 & isaRadNumber(ordinal)):
                lidi.at[index, 'Radnumer'] = ordinal
                lidi.at[index, 'Nafn'] = club





def create_duplicated_entries(duplication_array):
    for index, row in duplication_array.iterrows():
        full_name = row['Nafn']
        first_name = full_name.split()[0]
        last_name = full_name.split()[::-1][0]

        # make name lowercase
        first_name_lowercase = first_name.lower()
        last_name_lowercase = last_name.lower()

        # encode icelandic letters to english
        first_name_to_english = unidecode.unidecode(first_name_lowercase)
        last_name_to_english = unidecode.unidecode(last_name_lowercase)

        # split birthday into year month and day and ignore second part (sec, min, hour)
        if (last_name_to_english != first_name_to_english):
            Fdagur_date = row['Fdagur'].split()[0] + "+" + last_name_to_english
        else:
            Fdagur_date = row['Fdagur'].split()[0] + "+" + "<MISSING>"

        if first_name_to_english in duplicate_dict.keys():
            if Fdagur_date in duplicate_dict[first_name_to_english].keys():
                #if first name and Fdagur (birthday) exist in dict then append to that key (birthday)
                duplicate_dict[first_name_to_english][Fdagur_date].append(
                    row.values)
            else:
                #if first name exists but Fdagur (birthday) does not exist in dict
                duplicate_dict[first_name_to_english][Fdagur_date] = [
                    row.values]
        else:
            #if Fdagur (birthday) does not exist in dict
            duplicate_dict[first_name_to_english][Fdagur_date] = [row.values]




def remove_single_entries(duplication_array):
    for key, values in duplication_array.items():
        # key = nafn ('ludvik')
        for birthday, arrays in dict(values).items():
            # only get duplicates that there exists 2 or more entries for a birthday
            if(len(arrays) > 1):
                # used for when joining teams table
                if key in dict_removed_single_entries.keys():
                    if birthday in dict_removed_single_entries[key].keys():
                        dict_removed_single_entries[key][birthday].append(
                            arrays)
                    else:
                        #if first name exists but Fdagur (birthday) does not exist in dict
                        dict_removed_single_entries[key][birthday] = arrays
                else:
                    dict_removed_single_entries[key][birthday] = arrays




def identifier_map_unique_ids(duplication_array):
    for key, value in duplication_array.items():
        #get key and arrays for each person
        for birthday, arrays in dict(value).items():
            #get each array for person
            new_key = key + "+" + birthday
            for item in arrays:
                if new_key in dict_name_entries.keys():
                    dict_name_entries[new_key].append(item[0])
                else:
                    dict_name_entries[new_key] = [item[0]]




def get_duplication_keys(duplication_array):
    for key, values in duplication_array.items():
        # key = nafn ('ludvik')
        for birthday, arrays in dict(values).items():
            for item in arrays:
                duplicate_ids_kept.append(item[0])




def team_member_entries(duplication_array):
    for index, row in duplication_array.iterrows():
        ids = row["EinstID"]
        if ids in duplicate_ids_kept:
            # now we only view ids that exist for duplicated people
            #print(ids)
            if ids in dict_duplicate_compare_team_members.keys():
                dict_duplicate_compare_team_members[ids].append(row.values)
            else:
                dict_duplicate_compare_team_members[ids] = [row.values]



def connect_members_to_team_data(duplication_array):
    for key, value in duplication_array.items():
        #print("<key>" + str(key) + " <value> " + str(value))
        for item in value:
            #print(item)
            if item in dict_duplicate_compare_team_members.keys():
                #print("<key>" + str(key) + " <item> " + str(item))
                for compare_arrays in dict_duplicate_compare_team_members[item]:
                    mot_id = compare_arrays[0]
                    lid_id = compare_arrays[1]
                    player_id = compare_arrays[2]
                    date = compare_arrays[3]
                    date_played = compare_arrays[3].split()[0]

                    temp = (str(date) + " " + str(mot_id) + " " +
                            str(lid_id) + " " + str(player_id))
                    if key in dict_einstaklingar_teammember_info.keys():
                        dict_einstaklingar_teammember_info[key].append(temp)
                    else:
                        dict_einstaklingar_teammember_info[key] = [temp]




def find_duplicates(key, nums):
    num_set = set()
    duplicates = set()
    no_duplicate = -1
    sorted_nums = sorted(nums)
    last_array_entry = ""
    for i in range(len(sorted_nums)):
        for j in range(i+1, len(sorted_nums)):

            # team one split
            #(str(date) + " " + str(mot_id) + " " + str(lid_id) +  str(player_id))

            sort_1 = sorted_nums[i].split()
            date_1 = sort_1[0]
            mot_id_1 = sort_1[2]
            team_id_1 = sort_1[3]
            einstaklings_id_1 = sort_1[4]
            date_time_str_1 = sort_1[0]+" "+sort_1[1]
            date_time_obj_1 = datetime.datetime.strptime(
                date_time_str_1, '%Y-%m-%d %H:%M:%S.%f')

            # team two split
            sort_2 = sorted_nums[j].split()
            date_2 = sort_2[0]
            mot_id_1 = sort_2[2]
            team_id_2 = sort_2[3]
            einstaklings_id_2 = sort_2[4]
            date_time_str_2 = sort_2[0]+" "+sort_2[1]
            date_time_obj_2 = datetime.datetime.strptime(
                date_time_str_2, '%Y-%m-%d %H:%M:%S.%f')

            # time difference between these two entries
            time_diff = (date_time_obj_2 - date_time_obj_1).total_seconds()/60

            match_length = 60
            # There exist two record for erla with the same einstaklingsid but different teams (6286 and 6285)
            # played 6.5 minutes apart
            # TODO: figure out how to handle that
            if((date_1 == date_2) and (time_diff < match_length) and (einstaklings_id_1 != einstaklings_id_2)):
                combined = [sorted_nums[i], sorted_nums[j]]
                if key in not_the_same_person.keys():
                    not_the_same_person[key].append(combined)
                else:
                    not_the_same_person[key] = [combined]

            else:
                if last_array_entry != sorted_nums[i]:
                    # Here are all the potential duplicates left after filtering
                    #combined = [sorted_nums[i], sorted_nums[j]]
                    if key in most_likely_same_person.keys():
                        most_likely_same_person[key].append(sorted_nums[i])
                    else:
                        most_likely_same_person[key] = [sorted_nums[i]]
                last_array_entry = sorted_nums[i]


def call_find_duplicates(duplication_array):
    for key, value in dict_einstaklingar_teammember_info.items():
        find_duplicates(key, value)


def people_abled_to_merge(duplication_array):
    temp_arr = []

    def merged_ids(key, nums):
        for compare_arrays in nums:

            sort_1 = compare_arrays.split()
            einstaklings_id_1 = sort_1[4]

            if key in merged_list.keys():
                if einstaklings_id_1 not in temp_arr:
                    #print(key)
                    #print(einstaklings_id_1)
                    merged_list[key].append(einstaklings_id_1)
                    temp_arr.append(einstaklings_id_1)
            else:
                merged_list[key] = [einstaklings_id_1]
                temp_arr.append(einstaklings_id_1)

    for key, value in duplication_array.items():
        merged_ids(key, value)
        temp_arr = []

### calling functions
# call def
correctRadNumbersFromEntries()
# call def
create_duplicated_entries(duplicated_fdagur_kyn_einstaklingar)
# call def
remove_single_entries(duplicate_dict)
# call def
identifier_map_unique_ids(dict_removed_single_entries)
# call def
get_duplication_keys(dict_removed_single_entries)
# call def
team_member_entries(lidsmenn)
# call def
connect_members_to_team_data(dict_name_entries)
# call def
call_find_duplicates(dict_einstaklingar_teammember_info)
# call def
people_abled_to_merge(most_likely_same_person)

### WRITE MERGE SUGGESTIONS TO FILE
# WRITE THESE RESULTS TO TXT FILE
merge_suggestion_for_people = (str(merged_list))
text_file = open("merge_suggestions.txt", "w")
text_file.write(merge_suggestion_for_people)
text_file.close()

# WRITE THESE RESULTS TO PICKLE FILE TO BE ABLE TO WORK WITH THEM AGAIN
# ONLY WORKS IN JUPYTER NOTEBOOK WITHOUT INSTALLING PACKAGES
#pickle_obj = open("merge_suggestions.pickle", "wb")
#pickle.dump(merged_list, pickle_obj)
#pickle_obj.close()

#duplicated people put into it's own csv to be browsed later
pd.DataFrame(duplicated_einstaklingar).to_csv("csv/new/duplicated-einstaklingar.csv", encoding='utf-8-sig')

#save as new csv inside csv/new
pd.DataFrame(domarar).to_csv("csv/new/blak-domarar.csv", encoding='utf-8-sig')
pd.DataFrame(einstaklingar).to_csv("csv/new/blak-einstaklingar.csv", encoding='utf-8-sig')
pd.DataFrame(forsvarsmenn).to_csv("csv/new/blak-forsvarsmenn.csv.csv", encoding='utf-8-sig')
pd.DataFrame(lidi).to_csv("csv/new/blak-lid.csv", encoding='utf-8-sig')
pd.DataFrame(lidimoti).to_csv("csv/new/blak-lidimoti.csv", encoding='utf-8-sig')
pd.DataFrame(lidsmenn).to_csv("csv/new/blak-lidsmenn.csv", encoding='utf-8-sig')
pd.DataFrame(lidsstjorar).to_csv("csv/new/blak-lidsstjorar.csv", encoding='utf-8-sig')
pd.DataFrame(mot).to_csv("csv/new/blak-mot.csv", encoding='utf-8-sig')
pd.DataFrame(thjalfarar).to_csv("csv/new/blak-thjalfarar.csv", encoding='utf-8-sig')
