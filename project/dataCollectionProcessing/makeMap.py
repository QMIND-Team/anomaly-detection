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

def plotNeighbourhoods():
    neighbourhoods = readShapes()
    for n in neighbourhoods:
        x,y = n[1].exterior.xy
        plt.plot(x,y)

def plotHouses():
    fin = open("KingstonHousesNadded.txt", 'r')
    for line in fin.readlines():
        lin = line.strip().split(',')
        point = Point((float(lin[7]), float(lin[8])))
        print(point)
        plt.plot(point.x, point.y, marker = 'o', markersize=1, color='red')
        # plt.plot(point)
    fin.close()


plotNeighbourhoods()
plotHouses()
plt.show()











