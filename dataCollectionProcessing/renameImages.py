'''
@author: Jacob Laframboise

A file desinged to rename images that are named in the format num__type.jpeg
If the images have missing numbers in the sequence, this will rename them to
eliminate the missing numbers and keep the order correct.
'''

import os

direcPath = r'/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/renamedcropped/'

print(os.listdir(direcPath))

newFileNameList = []
for filename in os.listdir(direcPath):
    splitName = filename.split('_')
    newFileNameList.append([int(splitName[0]), splitName[1]])

newFileNameList.sort()

i = 0
for file in newFileNameList:
    file[0] = str(file[0])
    fileName = '_'.join(file)
    print(fileName)

    dst = str(i) + "_streetview" + ".jpeg"
    src = direcPath + fileName
    dst = direcPath + dst

    # rename() function will
    # rename all the files
    os.rename(src, dst)
    i += 1
