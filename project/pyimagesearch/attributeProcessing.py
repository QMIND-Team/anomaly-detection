from sklearn.preprocessing import LabelBinarizer 
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
import numpy as np 
import glob 
import cv2
import os 

def get_house_attributes(filePath):
	cols = ["price","neighbourhood","POI"]
	tempcols = ["price", "neighbourhood"]
	df = pd.read_csv(filePath, sep="," , usecols = tempcols)

	return df

def process_house_attributes(df, train, test):
	continuous = ["POI"]

	#Adjusts continuous values
	scaler = MinMaxScaler()
	trainCont = scaler.fit_transform(train[continuous])
	testCont = scaler.fit_transform(test[continuous])

	#one-hot encode neighbourhoods 
	nbdBinarizer = LabelBinarizer().fit(df[neighbourhood])
	trainCategories = nbdBinarizer.transform(train['neighbourhood'])
	testCategories = nbdBinarizer.transform(test['neighbourhood'])

	trainX = np.hstack([trainCategories, trainCont])
	testX = np.hstack([testCategories, testCont])

	return(trainX,testX)

def load_house_images(df, inputPath):
	images = []

	for i in df.index.values: 
		basePath = os.path.sep.join([inputPath, "{}_*".format(i)])
		print(basePath)
		housePaths = sorted(list(glob.glob(basePath)))

		inputImages = []
		outputImage = np.zeros((64,32,3) , dtype ="uint8")
		for housePath in housePaths:
			image = cv2.imread(housePath)
			image = cv2.resize(image,(32,32))
			inputImages.append(image)
		print(len(inputImages))
		outputImage[0:32, 0:32] = inputImages[0]
		outputImage[32:64, 0:32] = inputImages[1]

		images.append(outputImage)

	return np.array(images)
