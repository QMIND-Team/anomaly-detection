'''
@author: Jacob Laframboise

This file is designed to process the dataset contained in two files,
one file being a list of rebuild costs and the other file being a file
of addresses that the rebuild costs pertain to.
'''


'''A function that takes in a list of address terms in a certain fromat and
returns the street number, name, and type. It performs some basic cleaning and
expansion of abbreviations. '''
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
                              'cr': 'crescent',
                              'ln': 'lane',
                              'ter': 'terrace',
                              'cir': 'circle',
                              'trl': 'trail',
                              'pky': 'parkway',
                              'lin': 'line',
                              'hwy': 'highway'}
    # expand abbreviations
    for x in range(len(addressParts)):
        if addressParts[x].lower() in shortToLongStreetTypes:
            addressParts[x] = shortToLongStreetTypes[
                addressParts[x].lower()].title()
    # the data is properly formatted without being a special case
    if len(addressParts) == 3:
        sNum = addressParts[0]
        sName = addressParts[1]
        sType = addressParts[2]
        return sNum, sName, sType
    # there is an extra terms because there was a multi word name etc.
    elif len(addressParts) > 3:
        # all possible street types
        fullStreetTypes = ['place', 'road', 'drive', 'avenue', 'crescent',
                           'street',
                           'way', 'boulevard', 'court', 'lane', 'terrace',
                           'circle', 'route',
                           'trail', 'parkway', 'line', 'Row', 'crossing',
                           'townline',
                           'private', 'gardens', 'rue', 'square', 'row',
                           'side road',
                           'highway']
        for partNo in range(len(addressParts)):
            # if that part is a street type
            if addressParts[partNo].lower() in fullStreetTypes:
                sType = addressParts[partNo].title()
                if sType not in ["Highway", 'Route']:
                    del addressParts[partNo]
                # get the number and name once type is gone
                sNum = addressParts[0]
                sName = ' '.join(addressParts[1:])
                return sNum, sName, sType
        print("Now sType found for line:")
        print(' '.join(addressParts))
    # there is no street type
    elif len(addressParts) == 2:
        sNum = addressParts[0]
        sName = addressParts[1]
        sType = 'None'
        return sNum, sName, sType


'''A function to read in the addresses from the respective file and parse the
addresses with the parseNumNameType function. It returns the list of lists
that contain the parsed parts. '''
def readAdresses(fPath="addresses.csv"):
    outLines = []
    f = open(fPath, "r")
    fatalErrorCount = 0
    print("ERROR LINES: -----------------------------------------")
    for line in f.readlines()[1:]:
        try:
            line = line.replace("\"", "").strip().replace(".", "")
            bigParts = line.split(",")
            # bad number of parts
            if len(bigParts) != 5:
                print("Error line too big/small")
                print(line)
                continue
            index, address, city, pCode, province = line.split(",")
            addressParts = address.split(" ")
            sNum, sName, sType = parseNumNameType(addressParts)

            # this is the format of all lists in outLines
            outLine = [index, sNum, sName, sType, city, province]
            outLines.append(outLine)
        except:
            fatalErrorCount += 1
            print("Fatal Error on line:")
            print(line)
    f.close()
    print("Number of fatal errors:")
    print(fatalErrorCount)
    return outLines


''' a function to add the rebuild costs of the houses to the lines, 
by getting input from file'''
def addVals(lines, fPath='vals.csv'):
    fvals = open(fPath, 'r')
    # format lines
    valsList = [x.strip().replace("\"", '').split(',') for x in
                fvals.readlines()[1:]]
    # insert into lines by the index of the house in lines corresponding
    # to the index in the vals list.
    for x in range(len(lines)):
        lines[x].insert(0, valsList[int(lines[x][0]) - 1][1])
    return lines


'''A function to filter out all of the houses that are not in kingston'''
def filterForKingston(lines):
    kingstonLines = []
    for line in lines:
        if line[-2].lower().replace(" ", '') == 'kingston':
            kingstonLines.append(
                [line[0], line[2], line[3], line[4], line[5], line[6]])
    return kingstonLines


''' A function to write the kingston house data to file.'''
def writeKingstonLines(kingstonLines, fPath='KingstonHouses.txt'):
    fout = open(fPath, 'w')
    for x in kingstonLines:
        fout.write(','.join(x) + "\n")
    fout.close()


'''A function to run all the functionality in this file, 
taking the path to the adresses file,the path to the vals file, and the 
desired output file name. Uses all the functions above.'''
def createKingstonHouseRebuildData(addressPath="addresses.csv",
                                   valPath='vals.csv',
                                   outPath='KingstonHouses.txt'):
    houses = readAdresses(addressPath)
    houses = addVals(houses, valPath)
    kingstonHouses = filterForKingston(houses)
    writeKingstonLines(kingstonHouses, outPath)


if __name__ == "__main__":
    createKingstonHouseRebuildData()
