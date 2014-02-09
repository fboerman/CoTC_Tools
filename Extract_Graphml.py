__author__ = 'williewonka'

import json


#the data is saved as dictionary of dictionaries with id as key. the items of the dictionary contain the name and a dictionary of children
#the children follow the same data structure
hierarchy = {}

#open the file
stream = open("Crisis of the Confederation Map Corrected.gml", "r")
file = stream.readlines()#preread all the lines to make it easier to jump in the file
stream.close()
# iterate through it
i = 0
nodes = 0
while i < len(file):
    if "node" in file[i]:
        nodes += 1
        #extract all the info, gid is id of parent
        i += 2
        id = file[i].strip("\t").split("\t")[1].strip("\n")
        i += 1
        name = file[i].strip("\t").split("\t")[1].strip("\n").strip('"').strip()
        isGroup = 0
        gid = None
        while i < len(file):
            if "isGroup" in file[i]:
                isGroup = 1
            elif "gid" in file[i]:
                gid = file[i].strip("\t").split("\t")[1].strip("\n")
            elif file[i] == "\t]\n":
                break
            i += 1
        # create the dataitem
        if isGroup:
            item = {
                'name' : name,
                'children' : {}
            }
        else:
            item = {
                'name' : name,
                'children' : None
            }
        if gid is None:#no parent so new top level item
            hierarchy[id] = item
        else:#has a parent
            #look for the parent
            if gid in hierarchy:#parent is in toplevel
                hierarchy[gid]['children'][id] = item
            else:
                #not in top hierarchy so iterate through all second level, the map never goes deeper than three levels so the parent has to be in here
                #if not then the item is dropped because the loop will finish and never save the item
                for key in hierarchy.keys():
                    value = hierarchy[key]
                    if gid in value['children']:
                        hierarchy[key]['children'][gid]['children'][id] = item
                        break
    i += 1
print("file parsed, " + str(nodes) + " nodes found")
dataobject = json.dumps(hierarchy)
print("json object created")
stream = open("provinces_hierarchy.json","w")
stream.writelines(dataobject)
stream.close()
print("json saved to file")