import urllib, os, json
from topSecretStuff import apiKey
from neighborhoods import getName

import json
from matplotlib import pyplot as plt


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
def getGeoCode(address):
    base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    addressformat = str(address[0]) + ' ' + address[1] + ' ' + address[2] + ', ' + address[3] + ', ' + address[4]
    addressURL = urllib.parse.quote_plus(addressformat)
    url = base + addressURL + apiKey
    response = urllib.request.urlopen(url)
    jsongeocode = response.read()
    data = json.loads(jsongeocode)
    print(data)
    lat = data['results'][0]['geometry']['location']['lat'] #Gets the latitude of an address
    long = data['results'][0]['geometry']['location']['lng'] #Gets the longitude of an address
    longlat = [long, lat]
    return longlat


#address1  = [8,"Birch","Avenue", "Kingston", "ON"]
#print(getGeoCode(address1))

f = open("houseDataCombined.csv", 'r')
for line in f.readlines()[1:10]:
    lin = line.strip().split(',')
    print(lin[1:max(5,len(lin))])
    longlat = getGeoCode(lin[1:max(5,len(lin))])
    point = Point(longlat)
    print(point)
    print(getName(point, ))

f.close()