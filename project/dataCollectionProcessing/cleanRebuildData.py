def parseNumNameType(addressParts):
    shortToLongStreetTypes = {'rd': 'road',
                              'pl': 'place',
                              'dr': 'drive',
                              'ave': 'avenue',
                              'ct': 'court',
                              'crt': 'court',
                              'st': 'street',
                              'blvd': 'boulevard',
                              'cres': 'crescent',
                              'cr':'crescent',
                              'ln': 'lane',
                              'ter': 'terrace',
                              'cir': 'circle',
                              'trl': 'trail',
                              'pky': 'parkway',
                              'lin':'line',
                              'hwy':'highway'}
    for x in range(len(addressParts)):
        if addressParts[x].lower() in shortToLongStreetTypes:
            addressParts[x] = shortToLongStreetTypes[addressParts[x].lower()].title()

    if len(addressParts) == 3:
        sNum = addressParts[0]
        sName = addressParts[1]
        sType = addressParts[2]
        return sNum, sName, sType
    elif len(addressParts) > 3:
        fullStreetTypes = ['place', 'road', 'drive', 'avenue', 'crescent',
                           'street',
                           'way', 'boulevard', 'court', 'lane', 'terrace',
                           'circle', 'route',
                           'trail', 'parkway', 'line', 'Row', 'crossing', 'townline',
                           'private', 'gardens', 'rue', 'square', 'row', 'side road',
                           'highway']
        for partNo in range(len(addressParts)):
            if addressParts[partNo].lower() in fullStreetTypes:
                sType = addressParts[partNo].title()
                if sType not in["Highway", 'Route']:
                    del addressParts[partNo]
                sNum = addressParts[0]
                sName = ' '.join(addressParts[1:])
                return sNum, sName, sType
        print("Now sType found for line:")
        print(' '.join(addressParts))
    elif len(addressParts)==2:
        sNum = addressParts[0]
        sName = addressParts[1]
        sType = 'None'
        #print("Uh oh, there are not enough parts to this address:")
        #print(' '.join(addressParts))
        return sNum, sName, sType


outLines = []

print("ERROR LINES: -----------------------------------------")
f = open("addresses.csv", "r")
fatalErrorCount = 0
for line in f.readlines()[1:]:
    try:
        line = line.replace("\"", "").strip().replace(".","")
        bigParts = line.split(",")
        if len(bigParts)!=5:
            print("Error line too big")
            print(line)
            continue
        index, address, city, pCode, province = line.split(",")
        addressParts = address.split(" ")

        sNum, sName, sType = parseNumNameType(addressParts)

        pCode = pCode.replace(" ", "")
        outLine = [index, sNum, sName, sType, city, province]
        outLines.append(outLine)
    except:
        fatalErrorCount+=1
        print("Fatal Error on line:")
        print(line)
f.close()

print("Number of fatal errors:")
print(fatalErrorCount)

#print("Success lines: _-----------------------------------------------------------")

#fout = open('output.txt', 'w')
#for x in outLines:
    #fout.write(','.join(x)+"\n")
#fout.close()


fvals = open("vals.csv", 'r')

valsList = [x.strip().replace("\"", '').split(',') for x in fvals.readlines()[1:]]

for x in range(len(outLines)):
    outLines[x].insert(0, valsList[int(outLines[x][0])-1][1])

kingstonLines = []
for line in outLines:
    if line[-2].lower().replace(" ", '')=='kingston':
        kingstonLines.append([line[0], line[2], line[3], line[4], line[5], line[6]])

fout = open('KingstonHouses.txt', 'w')
for x in kingstonLines:
    fout.write(','.join(x)+"\n")
fout.close()

