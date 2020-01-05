# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:34:04 2019

@author: Colin Cumming, Jacob Laframboise
"""
from sklearn.preprocessing import MinMaxScaler

# import from folder
from pyimagesearch import attributeProcessing
from pyimagesearch import models

from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import concatenate
import numpy as np
import argparse
import locale
import os
import matplotlib.pyplot as plt

# paths
thisModulePath = os.path.abspath(__file__)
parentFolder = os.path.dirname(thisModulePath)
dataFolder = os.path.join(parentFolder, 'data')
inputPathHouseData = os.path.join(dataFolder, 'FINALDATASET.csv')
houseImagesPath = os.path.join(dataFolder, 'Images')

print("[INFO] loading numerical house data...")
df = attributeProcessing.get_house_attributes(inputPathHouseData)

# load the house images and normalize them
print("[INFO] loading house images...")
images = attributeProcessing.load_house_images(df, houseImagesPath)
images = images / 255.0

print("[INFO] processing data...")
split = train_test_split(df, images, test_size=0.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX) = split

# max scaling for prices
maxPrice = trainAttrX["price"].max()
trainY = trainAttrX["price"] / maxPrice
testY = testAttrX["price"] / maxPrice

# split numerical data
(trainAttrX, testAttrX) = attributeProcessing.process_house_attributes(df, trainAttrX, testAttrX)

# convert to numpy arrays from pandas Series
trainY = trainY.to_numpy()
testY = testY.to_numpy()

# create models for numerical and image data
mlp = models.create_mlp(trainAttrX.shape[1], regress=False)
cnn = models.create_cnn(32, 64, 3, regress=False)
print(type(mlp))
print(type(cnn))

# create a model to merge outputs of mlp and cnn
combinedInput = concatenate([mlp.output, cnn.output])

x = Dense(4, activation="relu")(combinedInput)
x = Dense(1, activation="linear")(x)

model = Model(inputs=[mlp.input, cnn.input], outputs=x)

# compile model
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(optimizer=opt, # metrics=["accuracy"],
              loss="mean_absolute_percentage_error")

# train the model
print("[INFO] training model...")
history = model.fit(
    [trainAttrX, trainImagesX], trainY,
    validation_data=([testAttrX, testImagesX], testY),
    epochs=30, batch_size=8)
# overfitting occurs after 30 epochs


# make predictions on the testing data
print("[INFO] predicting house prices...")
preds = model.predict([testAttrX, testImagesX])


# graph loss over training
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Learning Curve')
plt.ylabel('Mean Absolute Percentage Error')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show(block=True)


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
