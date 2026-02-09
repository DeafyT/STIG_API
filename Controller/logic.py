from .Configurations import configuration
import os

#Collect appropriate files. If a list_search is provided, it will find that list
#otherwise, it will return all lists
def list_files(list_search=None):
    files = os.listdir(configuration.stig_location)
    targets = []

    if list_search is not None:
        list_search = list_search.replace(" ", "_") #replaces spaces with underscore to match file names
        for file in files:
            if list_search in file:
                targets.append(os.path.join(configuration.stig_location, file))
    else:
        for file in files:
            targets.append(os.path.join(configuration.stig_location, file))
    return targets

#Ensure that the STIG Group ID is formatted correctly
def stig_id_formatter(stig_id):
    try:
        id = int(stig_id)
        stig_id = f"V-{id}"
        return stig_id
    except:
        if "v-" in stig_id:
            return stig_id.replace("v-", "V-")
        else:
            return stig_id

#Search for a STIG. Function will call list_files to get the list of files needed
#If stig_list is None, all files will be searched. Otherwise, the specific file will be searched
def find_stig(stig_id, stig_list=None):
    targets = list_files(stig_list)
    stig_id = stig_id_formatter(stig_id)

    for target in targets:
        trigger = False
        stop = False
        stig_data = ''
        with open(target, 'r') as f:
            for line in f:
                if f'<Group id="{stig_id}">' in line:
                    trigger = True
                if trigger:
                    stig_data += line
                    if '</Group>' in line:
                        if stig_id not in line:
                            stop = True
                            trigger = False
                            break
            if stop:
                break
    end_mark = "</Group>"
    index = stig_data.find(stig_id)
    stig_data = stig_data[index:]
    index = stig_data.find(end_mark)
    stig_data = stig_data[:index + 8]

    return stig_data

#Search a STIG list for keywords and return all STIGs with the keywords
def keyword_search(keywords, stig_list):
    target = list_files(stig_list)
    if len(target) > 1:
        return "Error, too many lists returned. Be more specific."
    elif len(target) == 0:
        return "Error, list not found."
    data = collect_stigs(target[0])
    for word in keywords:
        data = iterable_search(word, data)

    return data

#Iterate through the keywords to shorten the STIGs to matching all keywords
def iterable_search(word, stig_data):
    stigs = []
    for d in stig_data:
        if word.lower() in d:
            stigs.append(d)
    return stigs

#Will collect the entire file and split it into a list. All STIGs returned
def collect_stigs(file):
    text = ''
    with open(file, 'r') as f:
        for line in f:
            text += line

    end_mark = "</Group>"
    data = text.split(end_mark)
    return data

