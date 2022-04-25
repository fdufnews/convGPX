#!/usr/bin/env python

""" convert a gpx file without time tags to a compatible Garmin one
fdufnews april 25th 2022
published under GPL-3.0 license
"""

#from argparse import ArgumentParser
import argparse

import xml.etree.ElementTree as ET
import time as T
from math import sqrt, cos, sin, acos, radians

version = '1.0'

# calcRadius
# compute earth radius for the current latitude
# input lat : latitude in rad
# output earth radius in km
def calcRadius(lat):
  polarRadius = 6356.752
  equatRadius = 6378.137
  excent = sqrt(equatRadius * equatRadius - polarRadius * polarRadius) / equatRadius
  
  rho = equatRadius * ( 1 - excent * excent)/(1 - excent * excent * sin(lat) * sin(lat))**(3/2)
  N   = equatRadius / sqrt(1 - excent * excent * sin(lat) * sin(lat))
  radius = sqrt(rho * N)
  return radius

# calctimeto
# compute time to go from olat,olon to lat,lon
# input olat,olon to lat,lon in degrees
# output time in seconds
def calctimeto(lat, lon, olat, olon, timekm):
  rlat = radians(lat)
  rolat = radians(olat)
  rlon = radians(lon)
  rolon = radians(olon)
  SA_B = acos(sin(rolat) * sin(rlat) + cos(rolat) * cos(rlat) * cos(rlon - rolon))
  earthRadius = calcRadius(rlat)
  dst = earthRadius * SA_B
  timeto = dst * timekm
  return timeto, dst

# CLI parser
# expects inputfile and output file
# an optionnal speed argument can also be added
parser = argparse.ArgumentParser(
  description='Convert a GPX file without time information to a GPX understandable by Garmin GPS V'+ version,
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('inputfile', action="store", help='name of the input file')
parser.add_argument('outputfile', action="store", help='name of the output file')
parser.add_argument('--speed', action="store", type=float, default=5.0, help='Speed in km/h')
args = parser.parse_args()

file_name = args.inputfile
file_name2 = args.outputfile
# time kilometer in seconds
timekm = 3600 / args.speed

# Opens the file and processes the XML data
tree = ET.parse(file_name)
ET.register_namespace('','http://www.topografix.com/GPX/1/0')
root = tree.getroot()

# number of trackpoint
count = 0
# cumul of distance
totaldist = 0
dist = 0
oldlat = 0
oldlon = 0
newlat =0
newlon = 0
timetrip = 0
# for each route point
#   gets latitude and longitude
#   creates a new time element
#   compute distance from previous coordinates and time for the trip
#   accumulate distance and time
#   insert new time in the time element
for elem in root.findall(".//*[@lat]"):
  newelem = ET.SubElement(elem,"time")
  newlat = float(elem.attrib['lat'])
  newlon = float(elem.attrib['lon'])
  if count==0:
    curtime = T.time()
  else:
    timetrip, dist = calctimeto(oldlat, oldlon, newlat, newlon, timekm)
    curtime += timetrip
    totaldist += dist
    
  text = T.strftime("%Y-%m-%dT%H:%M:%S.000Z", T.gmtime(curtime))
  newelem.text = text
  count += 1
#  print('{}\toldlat {}\toldlon {}\tnewlat {}\tnewlon {}\tdelta {}\tdist {}\ttime {}'.format(count, oldlat, oldlon, newlat, newlon, dist, totaldist, text))
  print('{:>4d}\tdist {:>8.4f}\ttime {:>10.4f}\tcumul {:>10.4f}\ttime {}'.format(count, dist, timetrip, totaldist, text))
  oldlat = newlat
  oldlon = newlon

#save XML data in the new file
tree.write(file_name2)


