#!/usr/bin/python
# -*- coding: utf-8 -*-

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar
# 14 rue de Plaisance, 75014 Paris, France
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO. 

from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from gzip import GzipFile
from cStringIO import StringIO
from zlib import decompress
from struct import unpack
from time import sleep
from datetime import timedelta, date, datetime
from libxml2 import readDoc, XML_PARSE_NOERROR, XML_PARSE_RECOVER

def get_id(station):
    return get_ids(station+"!")[0]

def search_ids(station):
    return get_ids(station+"?")

def get_ids(query):
    result = list()
    req = Request("http://railnavigator.bahn.de/bin/rnav/query.exe/dn",
                '<?xml version="1.0" encoding="UTF-8" ?><ReqC ver="1.1" prod="String" lang="DE"><MLcReq><MLc n="%s" t="ST" /></MLcReq></ReqC>'%query,
                {"User-Agent":"Java/1.6.0_0"})
    root = readDoc(urlopen(req).read(), None, "iso-8859-1", XML_PARSE_NOERROR | XML_PARSE_RECOVER).children
        # <MLc t="ST" n="Bahlen Germann "Bahler Buur", Dinklage" i="A=1@O=Bahlen Germann "Bahler Buur", Dinklage@X=81
        # grrrrrrrrr - too stupid to escape their xml!!!!
    for child in root.children.children:
        if child.properties:
            for p in child.properties:
                if p.type == "attribute" and p.name == "i":
                    tokens = p.content.strip('@').split("@")
                    d = dict()
                    for t in tokens:
                        key, value = t.split("=", 1)
                        d[key] = value
                    result.append({"O":d["O"], "X":int(d["X"]), "Y":int(d["Y"]), "L":int(d["L"])})
    return result

infile = open("cities.txt", "r")
outfile = open("coordinates.txt", "w")

for city in infile:
    print city,
    for station in search_ids(city):
        outfile.write("%s\t%s\t%s\t%s\n"%(station["O"], station["X"], station["Y"], station["L"]))
    sleep(10)

infile.close()
outfile.close()
