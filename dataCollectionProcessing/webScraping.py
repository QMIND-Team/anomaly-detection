import requests
from bs4 import BeautifulSoup as bs
from topSecretStuff import url

# retrieval and cleaning functions -----------------------------------------

def getHouseData(url):
    houseDataList = []
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    for house in soup.findAll('div', attrs={'class': 'card__body'}):
        houseData = house.text.strip().split()[:-3]

        # check for highway 15 problem
        if houseData[2].lower()=='highway':
            houseData[2], houseData[3] = houseData[2]+" "+houseData[3], 'Highway'

        # remove money symbol and commas from price
        houseData[0]=houseData[0].replace(",", "").replace("$", "")
        # remove money symbol and commas from city
        houseData[-2] = houseData[-2].replace(",", "")

        # remove the "City of Kingston" naming
        for x in range(len(houseData)-2):
            if houseData[x].lower()=='city' and houseData[x+1].lower()=='of':
                del houseData[x]
                del houseData[x]
        if len(houseData)!=6:
            #print(houseData)
            pass
        if 'Lot' not in houseData and houseData not in houseDataList:
            houseDataList.append(houseData)
    return houseDataList



shortToLongStreetTypes = {'rd':'road',
               'pl':'place',
               'dr':'drive',
               'ave':'avenue',
               'ct':'court',
               'crt':'court',
               'st':'street',
               'blvd':'boulevard',
               'cres':'crescent',
               'ln':'lane',
                'ter':'terrace',
                'cir':'circle',
                'trl':'trail'}

fullStreetTypes = ['place', 'road', 'drive', 'avenue', 'crescent', 'street', 'way', 'boulevard', 'court', 'lane', 'terrace', 'cirlce', 'trail']

def replaceShortWithLong(houseList):
    for house in houseList:
        for datumNum in range(len(house)):
            if house[datumNum].lower() in shortToLongStreetTypes:
                house[datumNum] = shortToLongStreetTypes[house[datumNum].lower()]
            elif house[datumNum].lower() in fullStreetTypes:
                house[datumNum] = house[datumNum].lower()
    return houseList

def combineStreetNames(houseList):
    for house in houseList:
        typeIndex = 0
        streetNoIndex = 0
        for x in range(len(house)):
            if house[x] in fullStreetTypes:
                typeIndex = x
            try:
                if int(house[x])<10000:
                    streetNoIndex=x
                    str(house[x])
            except:
                pass
            if typeIndex !=0 and streetNoIndex!=0 and typeIndex-streetNoIndex>2:
                house[streetNoIndex+1:typeIndex] = [' '.join(house[streetNoIndex+1:typeIndex])]
                break
    return houseList

def checkIfUnit(house):
    for data in house:
        if "#" in data:
            return True
    return False

def removeUnits(houseList):
    for x in range(len(houseList)-1, 0, -1):
        if checkIfUnit(houseList[x]):
            del houseList[x]
    return houseList

def removeTooCheap(houseList):
    for house in houseList:
        if int(house[0])<100000:
            del house
    return houseList

def fixEastWest(houseList):
    direcList = ['west', 'north', 'south', 'east', 'e', 'w', 's', 'n']
    direcDict = {'e':'east', 'w':'west', 's':'south', 'n':'north',
                 'west':'west', 'north':'north', 'south':'south', 'east':'east'}
    for house in houseList:
        if house[-3].lower() in direcList:
            house[2] = house[2] + ' '+direcDict[house[-3].lower()]
            del house[-3]
    return houseList


# ------------------------ main area -------------------------------------


front = url[:55]
end = url[55:]
urlList = [front+str(x)+"/" +end for x in range(2,9)]
urlList.insert(0, url)

allHouseData = []
for url in urlList:
    houseDataOnPage = getHouseData(url)
    for house in houseDataOnPage:
        if house not in allHouseData:
            allHouseData.append(house)
            #print(house)

allHouseData= replaceShortWithLong(allHouseData)

allHouseData=combineStreetNames(allHouseData)

allHouseData = removeUnits(allHouseData)

allHouseData = removeTooCheap(allHouseData)

allHouseData = fixEastWest(allHouseData)

# ---------------- output area -------------------------------------
f = open('houseData.txt', 'w')
for x in allHouseData:
    print(x)
    f.write(','.join(x)+"\n")

#print(allHouseData)
# for x in allHouseData:
#     #print(x)
#     pass
# print(len(allHouseData))
#
#
# for x in allHouseData:
#     if len(x)!=6:
#         print(x)