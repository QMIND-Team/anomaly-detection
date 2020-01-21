# import the necessary packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model



def create_mlp(dim, regress=False):
	# define our MLP network
	model = Sequential()
	model.add(Dense(8, input_dim=dim, activation="relu"))
	model.add(Dense(4, activation="relu"))

	# check to see if the regression node should be added
	if regress:
		model.add(Dense(1, activation="linear"))

	# return our model
	return model

def create_cnn(width, height, depth, filters = (16,32,64), regress = False):

	inputShape = (height, width, depth)
	chanDim = -1

	inputs = Input(shape=inputShape)

	for (i,f) in enumerate(filters):

		if i == 0:
			x = inputs

		x = Conv2D(f,(3,3), padding ="same")(x)
		x = Activation("relu")(x)
		x = BatchNormalization(axis = chanDim)(x)
		x = MaxPooling2D(pool_size = (2,2))(x)

	x = Flatten()(x)
	x = Dense(16)(x)
	x = Activation("relu")(x)
	x = BatchNormalization(axis = chanDim)(x)
	x = Dropout(0.5)(x)

	x = Dense(4)(x)
	x = Activation("relu")(x)

	if regress:
		x = Dense(1,activation = "linear")(x)

	model = Model(inputs,x)
	return model 