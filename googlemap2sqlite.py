#!/usr/bin/env python3

import urllib.request   # to open URLs
import sys              # for commandline arguments

if 2 != len(sys.argv):
    sys.exit(1)

kmlrequest = urllib.request.urlopen(sys.argv[1] + '&output=kml')
print(kmlrequest.read())
