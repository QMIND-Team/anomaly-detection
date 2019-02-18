from sklearn.preprocessing import LabelBinarizer 
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
import numpy as np 
import glob 
import cv2
import os 

def get_house_attributes(filePath):
	cols = ["price","neighbourhood","POI"]
	df = pd.read_csv(filePath,sep=",", header = TRUE , usecols = cols)

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
