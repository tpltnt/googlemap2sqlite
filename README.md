googlemap2sqlite
================

Dump coordinates and descriptions from a [Google map](https://en.wikipedia.org/wiki/Google_maps) (KML 2.2) into a [sqlite](http://sqlite.org/) database. The coordinates are expressed in decimal degrees following the World Geodetic System of 1984 (WGS84). This scraper is mostly useful for data liberation and automated processing.
It creates two tables: places and coordinates. The [SQL](https://en.wikipedia.org/wiki/SQL) statements for their creation are
```
CREATE TABLE IF NOT EXISTS places (
  pid INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
)
```
```
CREATE TABLE IF NOT EXISTS coordinates (
  cid INTEGER PRIMARY KEY NOT NULL,
  pid INTEGER NOT NULL,
  longitude REAL NOT NULL,
  latitude REAL NOT NULL,
  altitude REAL
)
```
* **pid**: place ID as a key across tables
* **name**: (commoon) name of the place, often contains address information
* **description**: CDATA often containing links to corresponding posts on tumblr
* **cid**: coordinate (tuple) ID, one place may have multiple coordinates (e.g. a polygon)
* **longitude**: the longitude of the point described by *cid*
* **latitude**: the latitude of the point described by *cid*
* **altitude**: the altitude of the point described by *cid*, often set to 0.0

License: AGPLv3


references
----------
* Keyhole Markup Language (KML)
  * [wikipedia](https://en.wikipedia.org/wiki/Keyhole_Markup_Language)
  * [Open Geospatial Consortium](http://www.opengeospatial.org/standards/kml/)
  * [Google Inc.](https://developers.google.com/kml/documentation/?csw=1)
* [WGS84](http://earth-info.nga.mil/GandG/publications/tr8350.2/tr8350_2.html), [EPSG:4326](http://spatialreference.org/ref/epsg/4326/)
* [sqlite](http://sqlite.org/)
