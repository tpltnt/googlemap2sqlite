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


def extract_coordinates(placemark):
    """
    Extract the coordinates and return an array of float objects [[long,lat,alt],...].
    One tripel of coordinates indicates a point, multiple enclose an area.

    :param placemark: Placemark tag as extracted from KML data
    :type placemark: xml.etree.ElementTree.Element
    :raises: TypeError
    """

    if not isinstance(placemark, etree.Element):
        raise TypeError("given place not of type 'xml.etree.ElementTree.Element'")

    coordinates = placemark.text.strip()
    if -1 == coordinates.find('\n'):
        # convert each element into float
        return [[float(x) for x in coordinates.split(',')]]
    else:
        data = []
        # seperate triples
        for triple in coordinates.split('\n'):
            # convert each triple to float
            data.append([float(x) for x in triple.strip().split(',')])
        return data
    return None # should never be returned


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

