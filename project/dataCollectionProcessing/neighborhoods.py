from matplotlib import pyplot as plt
import urllib, os, json
from topSecretStuff import apiKey

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def readShapes():
    nList = []
    with open('neighbourhoods.json') as json_file:
        data = json.load(json_file)
        del data[6]
        count=0
        for n in data:
            points = n['fields']['geo_shape']['coordinates']
            while len(points)==1:
                if len(points)==2:
                    break
                points = points[0]
            if len(points)!=2:
                polygon = Polygon(points)
                name = n['fields']['name']
                #print(name)
                nList.append([name, polygon])
                count+=1
    return nList

            #nList.append(polygon)

def getGeoCode(address):
    base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    addressformat = str(address[1]) + ' ' + address[2] + ' ' + address[3] + ', ' + 'Kingston' + ', ' + 'Ontario'
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

def getName(p, neighbourhoods):
    for n in neighbourhoods:
        if n[1].contains(p):
            return n[0]
    return "Neighbourhood Unknown"




'''

neighbourhoods = readShapes()

for n in neighbourhoods:
    x,y = n[1].exterior.xy
    plt.plot(x,y)
    #plt.show()
#plt.show()


cp = Point(-76.65, 44.32)
plt.plot(-76.65, 44.32, marker='o', markersize=3, color="red")
#plt.plot(cp)
plt.show()

print(getName(cp, neighbourhoods))

f = open("cleanHouseDataCombined.csv", 'r')
outLines = []
for line in f.readlines()[1:]:
    lin = line.strip().split(',')
    print(lin[1:max(5,len(lin))])
    try:
        longlat = getGeoCode(lin[1:max(5,len(lin))])
        point = Point(longlat)
        print(point)
        nName = getName(point, neighbourhoods)
        lin.append(nName)
    except:
        lin.append("Unknown Neighbourhood")
    outLine = ','.join(lin)+"\n"
    outLines.append(outLine)
f.close()

f2 = open('houseDataCombinedNAdded.csv', 'w')
f2.writelines(outLines)
f2.close()

'''


def addNeighbourhoods(fileName):
    f = open(fileName, 'r')
    houses = [x.strip().split(',') for x in f.readlines()[1306:]]
    f.close()

    neighbourhoods = readShapes()
    for n in neighbourhoods:
        x, y = n[1].exterior.xy
        plt.plot(x, y)
        # plt.show()
    # plt.show()
    fout = open("KingstonHousesNadded2.txt", 'w')
    for house in houses:
        try:
            longlat = getGeoCode(house)
            point = Point(longlat)
            plt.plot(point.x, point.y, marker='o', markersize=3, color="red")
            #print(point)
            nName = getName(point, neighbourhoods)
            house.append(nName)
            house.append(str(longlat[0]))
            house.append(str(longlat[1]))
            fout.write(','.join(house)+"\n")
        except:
            print("Failed to get a name. -----------------------------------")
    plt.show()
    fout.close()

addNeighbourhoods("KingstonHouses.txt")
