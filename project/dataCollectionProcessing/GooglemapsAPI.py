#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:03:07 2019

@author: levistringer
"""

import urllib, os, json, csv

key = "&key=" + "AIzaSyDqaebtF2JXcBsZUILZHwq6laDy2Zaw1cg" #API key

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

def getStreetView(address,row):
    loc = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Satellite-View' #Local location to save images
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    geocode = getGeoCode(address)
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + key
    file = str(row) + "streetview" + ".jpeg"
    urllib.request.urlretrieve(url, os.path.join(loc,file))
    
    
def getSatView(address,row):
    loc = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Street-View' #Local location to save images
    base = "https://maps.googleapis.com/maps/api/staticmap?&center="
    geocode = getGeoCode(address)
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + "&zoom=19&size=400x400&maptype=satellite" + key
    file = str(row) + "satellite" + ".jpeg"
    urllib.request.urlretrieve(url, os.path.join(loc,file))


def getAllSatImages(fileName):
    with open(fileName) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        address = []
        for row in csv_reader:
            address.append(row[1])
            address.append(row[2])
            address.append(row[3])
            address.append(row[4])
            address.append(row[5])
            getSatView(address,row_count)
            row_count += 1
            address.clear()
            
def getAllStreetImages(fileName):
    with open(fileName) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        address = []
        for row in csv_reader:
            address.append(row[1])
            address.append(row[2])
            address.append(row[3])
            address.append(row[4])
            address.append(row[5])
            getStreetView(address,row_count)
            row_count += 1
            address.clear()

getAllStreetImages('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/houseDataCombinedNAdded.csv')