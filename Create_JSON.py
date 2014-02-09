__author__ = 'williewonka'

import os
import json
import encoding


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
        provincename = "provinces/" + filename
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

#main
Provinces()
# Dynasties()