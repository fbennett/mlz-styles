#!/usr/bin/python

import json
import sys

filename = sys.argv[1]

ifh = open(filename)
obj = json.load(ifh)

newmap = {}
for key in obj:
    newmap[key] = {}
    for kkey in obj[key]:
        if key == "institution":
            val = obj[key][kkey]["value"]
        else:
            val = obj[key][kkey]
        val = val.replace(u"\u2019", "'")
        newmap[key][val] = kkey

ofh = open("%s.new" % filename, "w+")
json.dump(newmap, ofh, indent=2)
