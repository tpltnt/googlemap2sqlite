#!/usr/bin/env python3

import xml.etree.ElementTree as etree  # for XML parsing
import urllib.request                  # to open URLs
import socket                          # to handle socket exception
import sys                             # for commandline arguments

if 2 != len(sys.argv):
    print("usage: " + str(sys.argv[0]) + " \"URL to google map\"")
    sys.exit(1)

try:
    kmlrequest = urllib.request.urlopen(sys.argv[1] + '&output=kml')
except urllib.error.URLError:
    print("URL error, maybe wrong?")
    sys.exit(2)
try:
    kmlstring = kmlrequest.read()
except ValueError:
    print("an error while requesting the data")
    sys.exit(3)

# root = etree.fromstring(kmlstring)
kmlfile = open("test.kml",'r')
root = etree.parse(kmlfile)

list_of_places = root.findall("./{http://earth.google.com/kml/2.2}Document/{http://earth.google.com/kml/2.2}Placemark")
for place in list_of_places:
    # extract the name
    element = place.find("./{http://earth.google.com/kml/2.2}name")
    name = element.text.strip()
    print(name)
    # extract coordinates
    element = place.find(".//{http://earth.google.com/kml/2.2}coordinates")
    print(element.__class__)
    coordinates = element.text.strip()
    print(coordinates)

