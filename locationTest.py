#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:03:07 2019

@author: levistringer
"""

import urllib, os, json



myloc = '/Users/levistringer/Documents/GitHub/Projects/Pictures'
key = "&key=" + "AIzaSyDqaebtF2JXcBsZUILZHwq6laDy2Zaw1cg" #got banned after ~100 requests with no key

filepath = os.path.join(myloc,'tester.jpeg')
image = "https://www.atlantisbahamas.com/media/Things%20To%20Do/Water%20Park/Beaches/Hero/Experiences_Beach.jpg"
"""
def GetStreet(Add,SaveLoc):
  base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
  MyUrl = base + urllib.quote_plus(Add) + key #added url encoding
  "fi = Add + ".jpg"
  "urllib.urlretrieve(MyUrl, os.path.join(SaveLoc,fi))
"""
Tests = ["457 West Robinwood Street, Detroit, Michigan 48203",
         "1520 West Philadelphia, Detroit, Michigan 48206",
         "2292 Grand, Detroit, Michigan 48238",
         "15414 Wabash Street, Detroit, Michigan 48238",
         "15867 Log Cabin, Detroit, Michigan 48238",
         "3317 Cody Street, Detroit, Michigan 48212",
         "14214 Arlington Street, Detroit, Michigan 48212"]

"""for i in Tests:
  GetStreet(Add=i,SaveLoc=myloc)
  """
  
  
  
def fileName(address,view):
    fi = str(address[0])+ address[1] + address[2] + address[3] + address[4] + view + ".jpeg"
    return fi

def getGeoCode(address):
    base = "https://maps.googleapis.com/maps/api/geocode/json?address=" 
    addressformat = str(address[0]) + ' ' + address[1] + ' ' + address[2] + ', ' + address[3] + ', ' + address[4]
    addressURL = urllib.parse.quote_plus(addressformat)
    url = base + addressURL + key
    #addressFormat = str(address[0])+ '+' 1600+Amphitheatre+Parkway,+Mountain+View,+CA"
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

"""
base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
MyUrl = base + urllib.parse.quote_plus("457 West Robinwood Street, Detroit, Michigan 48203") + key #added url encoding
Birch = "https://maps.googleapis.com/maps/api/streetview?size=300x150&scale=1&location=44.230442,-76.501021" + key
BirchSat = "https://maps.googleapis.com/maps/api/staticmap?&location=44.230442,-76.501021&size=400x400&maptype=satellite" + key
test = "https://maps.googleapis.com/maps/api/staticmap?&center=44.230442,-76.501021&zoom=18&size=400x400&maptype=satellite"+ key


#urllib.request.urlretrieve(Birch, os.path.join(myloc,"Birch.jpeg"))
#urllib.request.urlretrieve(BirchSat, os.path.join(myloc,"BirchSat.jpeg"))
urllib.request.urlretrieve(test, os.path.join(myloc,"test.jpeg"))
"""

address  = [8,"Birch","Avenue", "Kingston", "ON"]
#addresstest = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
#url="https://maps.googleapis.com/maps/api/geocode/json?address=" + addresstest + key getGeoCode(address))
getStreetView(address)
getSatView(address)
