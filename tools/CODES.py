#!/usr/bin/python

import csv,sys

c = csv.reader(open("codes.csv", "r"))

for row in c:
    print "   \"%s\":\"%s\"," % (row[6],row[5])
    