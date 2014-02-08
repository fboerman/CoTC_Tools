__author__ = 'williewonka'

import os
from fuzzywuzzy import fuzz

#open the streams
streamin = open("Crisis of the Confederation Map.gml", "r")
streamout = open("Crisis of the Confederation Map Corrected.gml", "w")

#read all the filenames in the province folder, use the one run for loop as a hack to get data from generator
# (no idea how those are supposed to work properly)
existing_provinces = {}
for info in os.walk('provinces'):
    files = info[2]
    for file in files:
        name = file.split("-")[1].strip().split(".")[0]
        id = int(file.split("-")[0].strip())
        existing_provinces[name] = id
    break

#iterate through file
cache = ""
for line in streamin:
    if "label" in line or "text" in line:#if there is a name in the current line
        name_ori = line.split('"')[1].strip("\n").strip()#isolate the name
        #check if the name is already correctly in the province files, then skip this one
        if name_ori in existing_provinces or "Sector" in name_ori:
            continue
        #if not see if there is a similar name in the list, if so than correct the name to this
        for province in existing_provinces:
            #caLculate fuzzy ratio
            ratio = fuzz.ratio(province, name_ori)
            if ratio > 75:
                if cache == "":
                    print("original name '" + name_ori + "' is maybe '" + province + "' with id '" + str(existing_provinces[province]) + "'")
                #ask for confirmation to change, ask only 1 per 2 changes because of the gml format everything is double (for label and text)
                if cache == "":
                    choice = input("Accept? (y/n) ")
                    if choice == "y":
                        streamout.write(line.replace(name_ori, province))
                        print("Changed line to: " + line.replace(name_ori, province).strip("\n"))
                    cache = choice
                else:
                    if cache == "y":
                        streamout.write(line.replace(name_ori, province))
                    cache = ""
    else:
        streamout.write(line)
        pass