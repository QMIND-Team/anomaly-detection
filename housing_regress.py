"""
QMIND - Google Street View Appraiser
Levi Stringer, Colin Cumming, Jacob Laframboise, Nick Merz

This file uses a multilayer perceptron on numerical house data
to estimate their value.
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
inputPath = os.path.join(dataFolder, 'FINALDATASET.csv')

# load and preprocess data
print("[INFO] loading numerical house data...")
df = attributeProcessing.get_house_attributes(inputPath)

print("[INFO] processing data...")
(train, test) = train_test_split(df, test_size=0.25, random_state=42)

# normalize data
maxPrice = train["price"].max()
trainY = train["price"] / maxPrice
testY = test["price"] / maxPrice

(trainX, testX) = attributeProcessing.process_house_attributes(df, train, test)

# convert to numpy arrays from pandas Series
trainY = trainY.to_numpy()
testY = testY.to_numpy()

# create model and compile
model = models.create_mlp(trainX.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

print("[INFO] training model...")
history = model.fit(trainX, trainY, validation_data=(testX, testY), epochs=200, batch_size=8)

print("[INFO] predicting house prices...")
preds = model.predict(testX)

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
