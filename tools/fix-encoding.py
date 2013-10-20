#!/usr/bin/python

import re

def replaceit (m):
    return unichr(int(m.group(1))).encode("utf-8")

txt = open("mlz-horitsu-henshu-sha-konwa-kai.csl").read().encode("utf-8")
txt = re.sub("&#([0-9]+);", replaceit, txt)

print txt
