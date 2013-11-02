#!/usr/bin/python

import re,sys

def replaceit (m):
    return unichr(int(m.group(1))).encode("utf-8")

def entityToChar (filename):
    txt = open(filename).read().encode("utf-8")
    txt = re.sub("&#([0-9]+);", replaceit, txt)
    return txt

if len(sys.argv) == 2:
    print entityToChar(sys.argv[1])
else:
    print "Script takes filename of a CSL style as sole argument"
