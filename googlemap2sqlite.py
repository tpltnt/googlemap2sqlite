#!/usr/bin/env python3

import xml.etree.ElementTree as etree  # for XML parsing
import urllib.request                  # to open URLs
import socket                          # to handle socket exception
import sys                             # for commandline arguments


def open_url(url):
    """
    Open URL and return ElementTree object.
    """
    if not isinstance(url,str):
        return None
    try:
        kmlrequest = urllib.request.urlopen(url + '&output=kml')
    except urllib.error.URLError:
        print("URL error, maybe wrong?")
        sys.exit(2)
    try:
        kmlstring = kmlrequest.read()
    except ValueError:
        print("an error while requesting the data")
        sys.exit(3)

    kmldata = etree.fromstring(kmlstring)
    return etree.ElementTree(kmldata)


def coordinates_str_to_triple(coordinates):
    """
    Convert coordinates string to triple.
    """

    if not isinstance(coordinates, str):
        raise TypeError("given coordinates not of type 'str'")
    pass


def extract_coordinates(place):
    """
    Extract the coordinates and return an array of float objects [[long,lat,alt],...].
    One tripel of coordinates indicates a point, multiple enclose an area.
    """

    if not isinstance(place, etree.Element):
        raise TypeError("given place not of type 'xml.etree.ElementTree.Element'")

    coordinates = place.text.strip()
    if -1 == coordinates.find('\n'):
        return []
    print(coordinates)
    return []


if 2 != len(sys.argv):
    print("usage: " + str(sys.argv[0]) + " \"URL to google map\"")
    sys.exit(1)


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
    coordinates = extract_coordinates(element)
    print(coordinates)

