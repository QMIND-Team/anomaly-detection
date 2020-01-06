import os
import pandas as pd

def dropRows(datafile, arrayfile):
	text_file = open(arrayfile, "r")
	indices = text_file.read().split(',')
	numbers = [int(i) for i in indices]
	
	#print(numbers)
	# importing pandas module 
	data = pd.read_csv(datafile, delimiter = ',')
	modDFObj = data.ix[numbers]
	print(len(modDFObj))
	modDFObj.to_csv(r'/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/dataCollectionProcessing/POICountsTester.csv')
 
# dropping passed values 
# display 

dropRows('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/dataCollectionProcessing/POICountsTester.csv',
	'/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/dataCollectionProcessing/indices.txt')