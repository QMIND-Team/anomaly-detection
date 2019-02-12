import json
from matplotlib import pyplot as plt


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

def getName(p, neighbourhoods):
    for n in neighbourhoods:
        if n[1].contains(p):
            return n[0]
    return "Neighbourhood Unknown"

print(getName(cp, neighbourhoods))



