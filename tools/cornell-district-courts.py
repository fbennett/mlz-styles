#!/usr/bin/python

import sys,os,re

from HTMLParser import HTMLParser

import urllib
import tidy
from cStringIO import StringIO
import json
import csv

# See also http://openjurist.org/us-court for an alternative source

urlTemplate = "http://www.law.cornell.edu/uscode/text/28/%s"

oCsv = csv.writer(open("codes.csv", "w+"))

abbrevs = json.load(open("../../mlz-bb/json/mlz-bluebook-19th-default-phrases.json"))["default"]["title-phrase"]

numbers = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4
}

class MyHTMLParser(HTMLParser):
    def __init__(self, **args):
        HTMLParser.__init__(self, **args)
        self.capture = False
        self.text = ""
        self.districts = []

    def handle_starttag(self, tag, attrs):
        if tag == "sectioncontent" and not self.text:
            self.capture = True
                    
    def handle_endtag(self, tag):
        if tag == "sectioncontent":
            self.capture = False

    def handle_data(self, data):
        if self.capture and data.rstrip():
            self.text += data
            if not data.strip().startswith("(") and data.strip().endswith("District"):
                self.districts.append(data.strip())

# instantiate the parser and fed it some HTML

# ar?

states = ["al","ak","az","ar","ca","co","ct","de","dc","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc","nd","oh","ok","or","pa","pr","ri","sc","sd","tn","tx","ut","vt","va","wa","wv","wi","wy"]

site = urllib.FancyURLopener()

ofh = open("codes.csv", "w+")

allcodes = []
for i in range(0, len(states), 1):
    state = states[i]
    parser = MyHTMLParser()
    io = StringIO()
    if i < 1:
        val = i + 81
    elif i == 1:
        val = "81a"
    else:
        val = i + 80
        
    url = urlTemplate % val
    pagetxt = site.open(url).read()
    site.close()
    parser.feed(pagetxt)
    text = parser.text
    io.write(text)
    io.seek(0)
    firstline = io.readline()
    mMulti = re.match("^(?:The )*((?:[A-Z][a-z]*(?: of |[, ]))+).*divided into *([a-zA-Z]+)", firstline)
    mOne = re.match("^(?:The )*((?:[A-Z][a-z]*(?: of |[, ]))+).*one judicial district", firstline)

    if mMulti:
        fullname = mMulti.group(1).strip().strip(",")
        if abbrevs.has_key(fullname):
            abbrev = abbrevs[fullname]
        else:
            abbrev = fullname
        line = [fullname, abbrev, state, numbers[mMulti.group(2)]]
        for district in parser.districts:
            if not re.match(".*[a-z].*", abbrev):
                dabbrev = "%s.D.%s" % (district[0],abbrev)
            else:
                abbrev = abbrev.replace(" ", "")
                dabbrev = "%s.D. %s" % (district[0],abbrev,)
            dcode = ".".join([x.lower() for x in district.split(" ")])
            code = [state,"%s" % dcode]
            code = ".".join(code)
            code = "us;federal;%s" % code
            newline = line + [district,dabbrev,code]
            allcodes.append(newline)
    elif mOne:
        fullname = mOne.group(1).strip().strip(",")
        if abbrevs.has_key(fullname):
            abbrev = abbrevs[fullname]
        else:
            abbrev = fullname
        if not re.match(".*[a-z].*", abbrev):
            dabbrev = "D.%s" % (abbrev,)
        else:
            dabbrev = "D. %s" % (abbrev,)
        code = "us;federal;%s" % state
        newline = [fullname,abbrev,state, 1, "", dabbrev,code]
        allcodes.append(newline)
    else:
        print firstline
        print "OUCH!"
        sys.exit()
    if not state == "dc":
        code = "us;%s" % state
        newline = [fullname, abbrev, state, 0, "", abbrev, code]
        allcodes.append(newline)
    io = None

longOrdinals = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth", "Eleventh"]
shortOrdinals = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th"]

for i in range(0, 11, 1):
    fullname = "%s Circuit" % longOrdinals[i]
    dabbrev = "%s Cir." % shortOrdinals[i]
    code = "us;federal;%s.circuit" % (shortOrdinals[i], )
    newline = [fullname, "", "", 0, "", dabbrev, code]
    allcodes.append(newline)

def sortme(a, b):
    alen = len(a[6].split(";"))
    blen = len(b[6].split(";"))
    if alen > blen:
        return 1
    elif alen < blen:
        return -1
    else:
        if a[6] > b[6]:
            return 1
        elif a[6] < b[6]:
            return -1
        else:
            return 0

allcodes.sort(sortme)

oCsv.writerows(allcodes)
