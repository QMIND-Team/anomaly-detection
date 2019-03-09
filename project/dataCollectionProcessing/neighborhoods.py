"""
@author: Jacob Laframboise

This file takes in data in json format from Open Data Kingston and the data
that was processed in cleanRebuildData. It will read in the shapes from
the json file and it will create a polygon for each. It will then get the
geo coordinates using a Google api, and based on that it can determine which
neighbourhood contains it and it will add the neighbourhood name and the
longitude, latitude to the file of house data.
"""

from matplotlib import pyplot as plt
import urllib, os, json
from topSecretStuff import apiKey

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def readShapes():
    """A function to read in the shaped and make polygons for each
    using shapely."""

    nList = []
    with open('neighbourhoods.json') as json_file:
        data = json.load(json_file)
        del data[6]
        count = 0
        for n in data:
            points = n['fields']['geo_shape']['coordinates']
            while len(points) == 1:
                if len(points) == 2:
                    break
                points = points[0]
            if len(points) != 2:
                polygon = Polygon(points)
                name = n['fields']['name']
                # print(name)
                nList.append([name, polygon])
                count += 1
    return nList


def getGeoCode(address):
    """A function that uses a Google api to get
    the geocoords from an address. """

    base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    addressformat = str(address[1]) + ' ' + address[2] + ' ' + address[
        3] + ', ' + 'Kingston' + ', ' + 'Ontario'
    addressURL = urllib.parse.quote_plus(addressformat)
    url = base + addressURL + apiKey
    response = urllib.request.urlopen(url)
    jsongeocode = response.read()
    data = json.loads(jsongeocode)
    print(data)
    lat = data['results'][0]['geometry']['location'][
        'lat']  # Gets the latitude of an address
    long = data['results'][0]['geometry']['location'][
        'lng']  # Gets the longitude of an address
    longlat = [long, lat]
    return longlat


def getName(p, neighbourhoods):
    """Gets the name based on if a point is in the neighbourhood polygon. """

    for n in neighbourhoods:
        if n[1].contains(p):
            return n[0]
    return "Neighbourhood Unknown"


def addNeighbourhoods(fileName):
    """ uses the above functions to add the nieghbourhood names to all
    of the houses in the kingston houses data file. """

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
            # print(point)
            nName = getName(point, neighbourhoods)
            house.append(nName)
            house.append(str(longlat[0]))
            house.append(str(longlat[1]))
            fout.write(','.join(house) + "\n")
        except:
            print("Failed to get a name. -----------------------------------")
    plt.show()
    fout.close()


if __name__ == "__main__":
    addNeighbourhoods("KingstonHouses.txt")
