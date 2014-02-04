__author__ = 'williewonka'

import os
import json

#first provinces
#provinces are stored as a list of dictionaries. each dictionary has the title culture and religion of the province
provinces = []
files = None
#read all the filenames in the province folder, use the one run for loop as a hack to get data from generator (no idea how those are supposed to work)
for info in os.walk('provinces'):
    files = info[2]
    break
#iterate through all the filenames
for filename in files:
    province = {} #create new dictionary for the province
    provincename = "provinces/" + filename
    for line in open(provincename,encoding="UTF-8"): #iterate through the file
        line = line.split("#")[0] #dump the comments, if it doesnt exist this will just select the whole line
        #check for the three main properties that we are interested in and extract the info from it
        if "title" in line:
            province['title'] = line.split("=")[1].strip()
        elif "culture" in line:
            province['culture'] = line.split('=')[1].strip()
        elif "religion" in line:
            province['religion'] = line.split('=')[1].strip()
    provinces.append(province)

#dump the list of dictionaries to a json file, this will overwrite existing json file
print("parsing provinces done")
JSON = json.dumps(provinces)
print("json created")
stream = open('provinces.json', 'w')
stream.writelines(JSON)
stream.close()
print("provinces updated")

#now dynasties
#for character generations it is best to have lists of available dynasteis per culture with their name and id
#so a dictionary with index culture name is used
#every culture entry has a list of dictionaries, these dictionaries contain name and id of dynastie

dyna_cultures = {}
#iterate through the file
file = open('00_dynasties.txt',encoding='UTF-8').readlines()
i = 0
while i < len(file): #use an index number for loop instead of iterating to allow line shifting within the loop
    line = file[i].split("#")[0] #drop the comments
    if "{" in line: # opening of new block
        #extract the properties line per line
        id = line.split("=")[0].strip()
        i += 1
        
        name = file[i].split("=")[1].strip().strip('"')
        i += 1
        
        culture = file[i].split("=")[1].strip().strip('"')
        i += 1
        
        if "used_for_random = no" in file[i]:#if this property is active then skip this block
            i += 1
            
            continue
        elif "}" in file[i]: #if block closes, create the data object and put it in right list
            dynastie = {
                "id" : id,
                "name" : name
            }
            culturelist = None
            try:#get the existing culture list, if non existing create empty list
                culturelist = dyna_cultures[culture]
            except:
                culturelist = []
            culturelist.append(dynastie)
            dyna_cultures[culture] = culturelist
            #done now iterate further
            i += 1
            
            continue
        else:#if neither closing nor pass property, rais an error for invalid file
            raise Exception("block at line " + i + " doesnt close properly")
    else:
        i += 1
        

#dump the created dataobject to a json file
print("parsing dynasties done")
JSON = json.dumps(dyna_cultures)
print("json created")
stream = open('dynasties_per_culture.json', 'w')
stream.writelines(JSON)
stream.close()
print('dynasties updated')