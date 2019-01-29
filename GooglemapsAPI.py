#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:03:07 2019

@author: levistringer
"""

import urllib, os, json


myloc = '/Users/levistringer/Documents/GitHub/Projects/Pictures' #Local location to save images
key = "&key=" + "KEY" #API key

filepath = os.path.join(myloc,'tester.jpeg')
    
def fileName(address,view):
    fi = str(address[0])+ address[1] + address[2] + address[3] + address[4] + view + ".jpeg"
    return fi

def getGeoCode(address):
    base = "https://maps.googleapis.com/maps/api/geocode/json?address=" 
    addressformat = str(address[0]) + ' ' + address[1] + ' ' + address[2] + ', ' + address[3] + ', ' + address[4]
    addressURL = urllib.parse.quote_plus(addressformat)
    url = base + addressURL + key
    response = urllib.request.urlopen(url)
    jsongeocode = response.read()
    data = json.loads(jsongeocode)
    lat = data['results'][0]['geometry']['location']['lat'] #Gets the latitude of an address
    long = data['results'][0]['geometry']['location']['lng'] #Gets the longitude of an address
    latlong = [lat, long]
    return latlong

def getStreetView(address):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    geocode = getGeoCode(address)
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + key
    file = fileName(address,"streetview")
    urllib.request.urlretrieve(url, os.path.join(myloc,file))
    
    
def getSatView(address):
    base = "https://maps.googleapis.com/maps/api/staticmap?&center="
    geocode = getGeoCode(address)
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + "&zoom=18&size=400x400&maptype=satellite" + key
    file = fileName(address,"satellite")
    urllib.request.urlretrieve(url, os.path.join(myloc,file))


address  = [8,"Birch","Avenue", "Kingston", "ON"]
address2 = [1216,"Unity", "Road", "Kingston", "ON"]
address3 = [213,"Millpond", "Place", "Kingston","ON"]
address4 = [375, "Bridge E", "St", "Belleville", "ON"]
getStreetView(address4)
getSatView(address4)
print(getGeoCode(address4))
