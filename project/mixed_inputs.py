# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:34:04 2019

@author: Colin Cumming
"""
from sklearn.preprocessing import MinMaxScaler

from pyimagesearch import attributeProcessing
from pyimagesearch import models
from sklearn.model_selection import train_test_split
from keras.layers.core import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import concatenate
import numpy as np
import argparse
import locale
import os
import matplotlib.pyplot as plt

inputPathHouse = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/FINALDATASET.csv'
df = attributeProcessing.get_house_attributes(inputPathHouse)
 
houseImages = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Images'
# load the house images and then scale the pixel intensities to the
# range [0, 1]
print("[INFO] loading house images...")
images = attributeProcessing.load_house_images(df, houseImages)
images = images / 255.0

print("[INFO] processing data...")
split = train_test_split(df, images, test_size=0.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX) = split

maxPrice = trainAttrX["price"].max()
trainY = trainAttrX["price"] / maxPrice
testY = testAttrX["price"] / maxPrice


(trainAttrX, testAttrX) = attributeProcessing.process_house_attributes(df,trainAttrX, testAttrX)

mlp = models.create_mlp(trainAttrX.shape[1], regress=False)
cnn = models.create_cnn(32, 64, 3, regress=False)
print(type(mlp))
print(type(cnn))
combinedInput = concatenate([mlp.output, cnn.output])

x = Dense(4, activation="relu")(combinedInput)
x = Dense(1, activation="linear")(x)

model = Model(inputs=[mlp.input, cnn.input], outputs=x)

opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(optimizer=opt, metrics=["accuracy"], loss="mean_absolute_percentage_error") #loss = 'binary_crossentropy')  try this later
 
# train the model
print("[INFO] training model...")
history = model.fit(
	[trainAttrX, trainImagesX], trainY,
	validation_data=([testAttrX, testImagesX], testY), #put back to 200 epochs
	epochs=10, batch_size=8)
# make predictions on the testing data
print("[INFO] predicting house prices...")
preds = model.predict([testAttrX, testImagesX])


#try and plot later
# print(history.history.keys()) 
# # summarize history for accuracy
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# # summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show(block=True)



# compute the difference between the *predicted* house prices and the
# *actual* house prices, then compute the percentage difference and
# the absolute percentage difference
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)
 
# compute the mean and standard deviation of the absolute percentage
# difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)


 
# finally, show some statistics on our model
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("[INFO] avg. house price: {}, std house price: {}".format(
	locale.currency(df["price"].mean(), grouping=True),
	locale.currency(df["price"].std(), grouping=True)))
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))