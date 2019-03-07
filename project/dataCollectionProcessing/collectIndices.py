
import os 
import glob 
import ntpath

def collectIndices(dir,pattern):
	indices = []
	for filename in glob.iglob(os.path.join(dir,pattern)):
		bName = ntpath.basename(filename)
		#print(bName)
		indice = bName.split('_')
		indices.append(indice[0])
	print(indice)
	ind_Out = open("indices.txt", "w")
	for number in indices:
		ind_Out.write(number)
		ind_Out.write(",")
	ind_Out.close

collectIndices('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/cropped',r'*.jpeg')
