"""
QMIND - Google Street View Appraiser
Levi Stringer, Colin Cumming, Jacob Laframboise, Nick Merz

This file uses a convolutional neural network on satellite and street view images
of houses to estimate their value.
"""

# imports
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import locale
import os
import matplotlib.pyplot as plt

# local folder imports
from pyimagesearch import attributeProcessing
from pyimagesearch import models

# paths
thisModulePath = os.path.abspath(__file__)
parentFolder = os.path.dirname(thisModulePath)
dataFolder = os.path.join(parentFolder, 'data')
inputPathHouse = os.path.join(dataFolder, 'FINALDATASET.csv')
inputPathImage = os.path.join(dataFolder, 'Images')

print("[INFO] loading prices...")
df = attributeProcessing.get_house_attributes(inputPathHouse)

# load and normalize the house images
print("[INFO] loading house images...")
images = attributeProcessing.load_house_images(df, inputPathImage)
images = images / 255.0

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
split = train_test_split(df, images, test_size=0.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX) = split

# find the largest house price in the training set and use it to
# scale our house prices to the range [0, 1] (will lead to better
# training and convergence)
maxPrice = trainAttrX['price'].max()  # changed from "price"
trainY = trainAttrX['price'] / maxPrice
testY = testAttrX['price'] / maxPrice

# convert to numpy arrays from pandas Series
trainY = trainY.to_numpy()
testY = testY.to_numpy()

# create our Convolutional Neural Network and then compile the model
# using mean absolute percentage error as our loss, implying that we
# seek to minimize the absolute percentage difference between our
# price *predictions* and the *actual prices*
model = models.create_cnn(32, 64, 3, regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

# train the model
print("[INFO] training model...")
history = model.fit(trainImagesX, trainY, validation_data=(testImagesX, testY),
                    epochs=30, batch_size=8)

# make predictions on the testing data
print("[INFO] predicting house prices...")
preds = model.predict(testImagesX)

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

# graph loss over training
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Learning Curve')
plt.ylabel('Mean Absolute Percentage Error')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show(block=True)

# finally, show some statistics on our model
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("[INFO] avg. house price: {}, std house price: {}".format(
    locale.currency(df["price"].mean(), grouping=True),
    locale.currency(df["price"].std(), grouping=True)))
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))
