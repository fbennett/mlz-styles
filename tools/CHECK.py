#!/usr/bin/python

import json
import sys

filename = sys.argv[1]

ifh = open(filename)
obj = json.load(ifh)

print "OK"