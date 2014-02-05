__author__ = 'williewonka'

import json

#load the json file
jsonfile = open("provinces_hierarchy.json", "r")
hierarchy = json.loads(jsonfile.readlines()[0])

stream = open("hierarchy.txt", "w")
def Print(line):
    print(line)
    stream.write(line + "\n")

#prints the map hierarchy
for id in hierarchy.keys():
    Print(hierarchy[id]['name']+":")
    for cid in hierarchy[id]['children'].keys():
        child = hierarchy[id]['children'][cid]
        if child['children'] is None:
            Print("\t"+child['name'])
        else:
            Print("\t"+child['name']+":")
            for ccid in child['children']:
                childofchild = child['children'][ccid]
                Print("\t\t"+childofchild['name'])

stream.close()