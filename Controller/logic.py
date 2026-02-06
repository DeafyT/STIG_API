import configuration
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

#Search for a STIG. Function will call list_files to get the list of files needed
#If stig_list is None, all files will be searched. Otherwise, the specific file will be searched
def find_stig(stig_id, stig_list=None):
    targets = list_files(stig_list)

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
    data = collect_stigs(target)
    stigs = []

    for d in data:
        if word in d:
            stigs.append(d)

    res = []

    for s in stigs:
        res.append(parser.stig_search_summarize(s))
        print()

    for r in res:
        if not res:
            print('There was an error processing some of the data')
    return "TODO: Implement function"


#Will collect the entire file and split it into a list. All STIGs returned
def collect_stigs(file):
    text = ''
    with open(file, 'r') as f:
        for line in f:
            text += line

    end_mark = "</Group>"
    data = text.split(end_mark)
    return data





print(find_stig("V-258241", "RHEL 9"))

