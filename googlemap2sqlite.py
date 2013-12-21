#!/usr/bin/env python3

import xml.etree.ElementTree as etree  # for XML parsing
import urllib.request                  # to open URLs
import socket                          # to handle socket exception
import sqlite3                         # to work a sqlite database
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


# get all the map data
kmlfile = open("test.kml",'r')
root = etree.parse(kmlfile)
list_of_places = root.findall("./{http://earth.google.com/kml/2.2}Document/{http://earth.google.com/kml/2.2}Placemark")
# set up the database connection
db_connection = sqlite3.connect('mapdata.db')
db_cursor = db_connection.cursor()

# create tables
db_cursor.execute('''
  CREATE TABLE IF NOT EXISTS places (
    pid INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT
  )''')
db_cursor.execute('''
  CREATE TABLE IF NOT EXISTS coordinates (
    cid INTEGER PRIMARY KEY NOT NULL,
    pid INTEGER NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    altitude REAL
  )''')

db_connection.commit()

for place in list_of_places:
    # extract ID (based on styleURL) -> own ID generation?
    element = place.find("./{http://earth.google.com/kml/2.2}styleUrl")
    place_id = element.text.strip().split('#style')[1]
    #print(place_id)
    # extract the name
    element = place.find("./{http://earth.google.com/kml/2.2}name")
    name = element.text.strip()
    print(name)
    # extract description
    element = place.find("./{http://earth.google.com/kml/2.2}description")
    description = element.text
    if None == description:
        description = ""
    description = description.strip()
    print(description)
    # extract coordinates
    element = place.find(".//{http://earth.google.com/kml/2.2}coordinates")
    coordinates = extract_coordinates(element)
    print(coordinates)

# final cleanup
db_cursor.close()
kmlfile.close()
