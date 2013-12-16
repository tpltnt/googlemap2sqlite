#!/usr/bin/env python3

import xml.etree.ElementTree as etree  # for XML parsing
import urllib.request                  # to open URLs
import sys                             # for commandline arguments

if 2 != len(sys.argv):
    print("usage: " + str(sys.argv[0]) + " \"URL to google map\"")
    sys.exit(1)

kmlrequest = urllib.request.urlopen(sys.argv[1] + '&output=kml')
kmlstring = kmlrequest.read()
root = etree.fromstring(kmlstring)
print(root.tag)
