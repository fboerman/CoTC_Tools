__author__ = 'williewonka'

#this tool checks if the provinces title exists and if this title has an owner

import json
# import random

#dictionary that keeps track of the number of existing members of a dynastie, that way no conflicts will emerge
existing_dynasties = {}
#id numbering: 001 + dynasty id
jsonfile = open("provinces.json", "r")
provinces = json.loads(jsonfile.readlines()[0])
# jsonfile = open("dynasties_per_culture.json", "r")
# dyna_per_culture = json.loads(jsonfile.readlines()[0])

#iterate through all the provinces
for province in provinces:
    #open the title document to see if the title is already to assigned to someone
    try:#check if the stream throws error, to see if the title exists yet
        filestream = open("titles/" + province["title"] + ".txt")
    except:
        print("title " + province["title"] + " does not exists")
    holder = False
    #iterate through file and look for a holder of the title
    for l in filestream:
        line = l.split("#")[0]
        if "holder" in line:
            holder = True
    if not holder:
        print("title " + province['title'] + " has no holder")
print("done")