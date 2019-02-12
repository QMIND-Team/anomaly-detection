f = open('houseDataCombined.csv', 'r')
lines = [x.strip().split(',') for x in f.readlines()]

for lineNum in range(len(lines)):
    for otherLineNum in range(len(lines)):
        if lines[lineNum][1]==lines[otherLineNum][1] and lines[lineNum][2]==lines[otherLineNum][2]:
            pass


newLines = []
for line in lines:
    dup = False
    if len(newLines)>0:
        for newLine in newLines:
            if newLine[1]==line[1] and newLine[2].title()==line[2].title():
                dup=True
                break
    if not dup:
        line[2] = line[2].title()
        newLines.append(line)

newLines = [','.join(x)+"\n" for x in newLines]

f2 = open('cleanHouseDataCombined.csv', 'w')
f2.writelines(newLines)
f2.close()
print('done')

