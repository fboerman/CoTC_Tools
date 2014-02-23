__author__ = 'williewonka'

import os
import json
import encoding
import argparse

def Provinces():
    #the provinces
    #provinces are stored as a dictionary of dictionaries. key is the province name, value has the following info:
    #culture, religion, the id, and a dictionary of baronies with name as key and dictionary of properties as value

    #read all the filenames in the province folder, use the one run for loop as a hack to get data from generator
    # (no idea how those are supposed to work properly)
    for info in os.walk('provinces'):
        files = info[2]
        break

    provinces = {}
    #iterate through all the filenames
    for filename in files:
        province = {} #create new dictionary for the province
        provincename = "./provinces/" + filename
        file = open(provincename,encoding="UTF-8").readlines()
        province['id'] = int(filename.split("-")[0].strip())
        #iterate through first part of the history file
        for i in range (0, len(file)):
            line = file[i].split("#")[0]
            #check for the three main properties that we are interested in and extract the info from it
            if "title" in line:
                province['title'] = line.split("=")[1].strip()
            elif "culture" in line:
                province['culture'] = line.split('=')[1].strip()
            elif "religion" in line:
                province['religion'] = line.split('=')[1].strip()
            elif "max_settlements" in line:
                province['max_settlements'] = int(line.split("=")[1].strip())
            elif "castle" in line or "temple" in line or "city" in line:
                #check if there already exists a list otherwise create it
                try:
                    baronies = province['baronies']
                except:
                    baronies = {}
                barony = {
                    'holding_type' : line.split("=")[1].strip()
                }
                baronies[line.split("=")[0].strip()] = barony
                province['baronies'] = baronies
            elif "1.1.1" in line:
                i += 1
                break
        #iterate through the building and holder block
        for j in range(i, len(file)):
            line = file[j].split("#")[0]
            if "}" in line:
                break
            elif "=" in line and "planet_survey" not in line: #if a building is referenced
                #extract type and which barony it is
                buildingtype = "xx" + line.split("=")[1].strip()[2:]
                barony = line.split("=")[0].strip()
                try:
                    #check the different categories of buildings
                    try:#Athmosphere
                        index = encoding.Atmosphere.index(buildingtype)
                        province['baronies'][barony]['Athmosphere'] = index
                    except ValueError:
                        try:#temperature
                            index = encoding.Temperature.index(buildingtype)
                            province['baronies'][barony]['Temperature'] = index
                        except ValueError:
                            try:#water
                                index = encoding.Water.index(buildingtype)
                                province['baronies'][barony]['Water'] = index
                            except ValueError:
                                try:#space station
                                    index = encoding.SpaceStation.index(buildingtype)
                                    province['baronies'][barony]['SpaceStation'] = index
                                except ValueError:
                                    try:#colonies
                                        index = encoding.Colony.index(buildingtype)
                                        province['baronies'][barony]['Colony'] = index
                                    except ValueError:
                                        try:#astroids
                                            index = encoding.Asteroids.index(buildingtype)
                                            province['baronies'][barony]['Asteroids'] = index
                                        except ValueError:
                                            #invalid building, raise error
                                            print("Invalid building type '" + buildingtype + "' at line " + str(j) + " in file '" + filename + "'")
                except KeyError:#faulty barony
                    print("None existing barony title '" + barony + "' in file '" + filename + "'")
        #done with parsing, put the province in the dictionary
        if len(filename.split("-")) == 2:
            provincename = filename.split("-")[1].split(".")[0].strip()
        else:
            items = filename.split("-")
            items.pop(0)
            provincename = "-".join(items).split(".")[0].strip()
        provinces[provincename] = province

    #dump the list of dictionaries to a json file, this will overwrite existing json file
    print("parsing provinces done")
    JSON = json.dumps(provinces)
    print("json created")
    stream = open('provinces.json', 'w')
    stream.writelines(JSON)
    stream.close()
    print("provinces updated")

def Dynasties():
    #dynasties
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

def Hierarchy():
    #reads the hierarchy.txt from the extraction of the gml to a json file
    #json file is a dictionary which holds dictionaries of the level beneath it three levels deep: top kingdoms duchies. a duchy entry holds a list
    #of counties

    hierarchy = {}
    #first open file and iterate through it
    file = open("hierarchy.txt", 'r').readlines()
    i = 0
    while i < len(file):
        print(str(i))
        line = file[i].strip('\n')
        kingdomname = line.strip(":")
        hierarchy[kingdomname] = {}
        j = i + 1
        while j <= len(file):#iterate through the kingdom
            print(str(j))
            line = file[j].strip(":").strip('\n')
            if line.count('\t') == 1:#is a duchy, put it in hierarchy and iterate through it
                duchyname = line.strip('\t').strip(":")
                if duchyname in hierarchy[kingdomname]: #if ducy already exists than throw an error
                    raise Exception("Double duchy entry at line " + str(j))
                hierarchy[kingdomname][duchyname] = {}
                #start loop for counties
                counties = []
                z = j + 1
                while z <= len(file):
                    print(str(z))
                    #if the line gives an error than end of file is reached, save the list and exit
                    try:
                        line = file[z].strip('\n')
                    except:
                        hierarchy[kingdomname][duchyname] = counties
                        j = z
                        break
                    if line.count('\t') == 2: #a county, add it to the list
                        counties.append(line.strip('\t'))
                    else: #no county so save the list and break from this loop
                        hierarchy[kingdomname][duchyname] = counties
                        j = z - 1
                        break
                    z += 1
            elif line.count('\t') == 0:#duchy ends so end this loop
                i = j - 1
                break
            else: #invalid tabs, throw error but check first for end of file
                raise Exception("Invalid tab count of " + str(line.count('\t')) + " on line " + str(j))

            if j == len(file):
                i = j
                break
            j += 1
        if i == len(file):
            break
        i += 1

    print("parsing hierarchy.txt done")
    JSON = json.dumps(hierarchy)
    print("json object created")
    stream = open('hierarchy.json', 'w')
    stream.writelines(JSON)
    stream.close()
    print("hierarchies updated")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tool that caches data to json objects')
    parser.add_argument('--operation', nargs='?', const=1, type=str, default='all', help='provinces/dynasties/hierarchy/all')

    choice = parser.parse_args().operation
    if choice == 'provinces':
        Provinces()
    elif choice == 'dyasties':
        Dynasties()
    elif choice == 'hierarchy':
        Hierarchy()
    elif choice == 'all':
        Provinces()
        Dynasties()
        Hierarchy()
    else:
        print('Invalid choice!')