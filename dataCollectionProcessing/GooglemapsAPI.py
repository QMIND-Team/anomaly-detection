#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:03:07 2019

@author: levistringer
"""

import urllib, os, json, csv, requests

key = "&key=" + "AIzaSyDqaebtF2JXcBsZUILZHwq6laDy2Zaw1cg" #API key
#key = "&key=" +'AIzaSyBRYp_U4eWl_3Ow-18cpPReZCWUAoPvhuo'
def fileName(address,view):
    fi = str(address[0])+ address[1] + address[2] + address[3] + address[4] + view + ".jpeg"
    return fi

def getGeoCode(address):
    base = "https://maps.googleapis.com/maps/api/geocode/json?address=" 
    print(address)
    #addressformat = str(address[0]) + ',' + address[1] + ',' + address[2] + ', ' + address[3] + ', ' + address[4]
    addressformat = str(address[1]) + ',' + address[2] + ',' + address[3] + ', ' + 'Kingston' + ', ' + 'Ontario'
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
    loc = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Street-View' #Local location to save images
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    #geocode = getGeoCode(address) Commented out because dataset has longitude latitude 
    geocode = []
    geocode.append(address[1])
    geocode.append(address[0])
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + key
    file = str(row) + "_streetview" + ".jpeg"
    urllib.request.urlretrieve(url, os.path.join(loc,file))
    
    
def getSatView(address,row):
    loc = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Satellite-View' #Local location to save images
    base = "https://maps.googleapis.com/maps/api/staticmap?&center="
    #geocode = getGeoCode(address)
    geocode = []
    geocode.append(address[1])
    geocode.append(address[0])
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + "&zoom=19&size=400x400&maptype=satellite" + key
    file = str(row) + "_satellite" + ".jpeg"
    urllib.request.urlretrieve(url, os.path.join(loc,file))
 

def getAllImages(fileName, view):
    with open(fileName) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        address = []
        firstline = True 
        for row in csv_reader:
            #if fcrstline: Takes in header 
             #   firstline = False
              #  continue
            #address.append(row[1])
            #address.append(row[2])
            #address.append(row[3])
            #address.append(row[4])
            #address.append(row[5])
            #address.append(row[6])
            print(row)
            address.append(row[7])
            address.append(row[8])
        
            if (view == 'sat'):
                getSatView(address,row_count)
            elif (view == "street"):
                getStreetView(address,row_count)
            row_count += 1
            address.clear()
            

def checkImage(line):
    base = "https://maps.googleapis.com/maps/api/streetview/metadata?size=1200x800&location="
    geocode = getGeoCode(line)
    url = base + str(geocode[0]) + ',' + str(geocode[1]) + key
    response = urllib.request.urlopen(url)
    jsoncode = response.read()
    data2 = json.loads(jsoncode)
    status = data2['status']
    if (status == 'ZERO_RESULTS') or (status == 'NOT_FOUND'):
        return False 
    else:   
        return True



def filterAddresses(filePath):
    unwanted_words = {'Mann', 'Terraverde','Millpond','Berkshire','Davenport','Cataraqui Westbrook','Brookedayle','Neighbourhood Unknown','Berkshire'}
    with open(filePath,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for line in reader:
            imageStatus = checkImage(line)
            print(line)       
            if set(line).isdisjoint(unwanted_words) and imageStatus:
                yield line
           
def write_output(filePath):
    fp = open('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/cleanedHouses1_2.csv', 'w')
    cw = csv.writer(fp,delimiter = ',')
    cw.writerows((line for line in filterAddresses(filePath)))

file = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/cleanedHouses.csv'   


getAllImages('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/dataCollectionProcessing/FINALDATASET2.csv','sat')
