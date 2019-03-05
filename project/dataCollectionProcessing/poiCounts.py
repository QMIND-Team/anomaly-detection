import pandas as pd
import math

houses = pd.read_csv('KingstonHousesNaddedComplete.csv')
points = pd.read_csv('simplePoints.csv')
count_list = []

def isInRange(pointscoords, housecoords, thresh):
    kmsperdegree = 111
    latdiff = (pointscoords[0] - housecoords[0])
    latdiff = round(latdiff, 7) * kmsperdegree
    longdiff = (pointscoords[1] - housecoords[1])
    longdiff = round(longdiff, 7) * kmsperdegree
    dist = math.sqrt(math.pow(latdiff, 2) + math.pow(longdiff, 2))
    if dist <= thresh:
        return True
    else:
        return False

poiList = []
for j, row in points.iterrows():
        currType = points.loc[j, 'type']
        if currType:
            houses[currType] = 0

pd.concat([houses, pd.DataFrame(columns=poiList)], sort=True)

for idx, row in houses.iterrows():
    print(idx)
    for j, row in points.iterrows():
        pointscoords = [points.loc[j, 'long'], points.loc[j, 'lat']]
        housecoords = [houses.loc[idx, 'long'], houses.loc[idx, 'lat']]
        poiType = points.loc[j, 'type']
        if isInRange(pointscoords, housecoords, 2):
            houses.loc[idx, poiType] = houses.loc[idx, poiType] + 1

houses.to_csv('poiCounts.csv', index=False)