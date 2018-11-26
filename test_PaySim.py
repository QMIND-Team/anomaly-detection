import pandas as pd
import numpy as np
from scipy import stats
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, precision_recall_curve
from sklearn.metrics import recall_score, classification_report, auc, roc_curve
from sklearn.metrics import precision_recall_fscore_support, f1_score
from sklearn.preprocessing import StandardScaler
from pylab import rcParams
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from sklearn.metrics import classification_report

RANDOM_SEED = 314
TEST_PCT = 0.15

df = pd.read_csv("sample.csv")
df.drop(['nameDest'], axis=1, inplace=True)
df.drop(['nameOrig'], axis=1, inplace=True)
df.drop(['newbalanceOrig'], axis=1, inplace=True)
df.drop(['oldbalanceDest'], axis=1, inplace=True)
# df.drop(['newbalanceDest'], axis=1, inplace=True)
df.drop(['isFlaggedFraud'], axis=1, inplace=True)
# df.drop(['oldbalanceOrg'], axis=1, inplace=True)

# Get one hot encoding of type
# one_hot = pd.get_dummies(df['type'])
# Remove type column
df.drop(['type'], axis=1, inplace=True)
# Join the encoded df
# df = df.join(one_hot)

df_norm = df
df_norm['amount'] = StandardScaler().fit_transform(df_norm['amount'].values.reshape(-1, 1))
df_norm['step'] = StandardScaler().fit_transform(df_norm['step'].values.reshape(-1, 1))
df_norm['oldbalanceOrg'] = StandardScaler().fit_transform(df_norm['oldbalanceOrg'].values.reshape(-1, 1))
df_norm['newbalanceDest'] = StandardScaler().fit_transform(df_norm['newbalanceDest'].values.reshape(-1, 1))
# df_norm['oldbalanceDest'] = StandardScaler().fit_transform(df_norm['oldbalanceDest'].values.reshape(-1, 1))
# df_norm['newbalanceOrig'] = StandardScaler().fit_transform(df_norm['newbalanceOrig'].values.reshape(-1, 1))
train_x, test_x = train_test_split(df_norm, test_size=TEST_PCT, random_state=RANDOM_SEED)
train_x = train_x[train_x.isFraud == 0]
train_x = train_x.drop(['isFraud'], axis=1)
test_y = test_x['isFraud']
test_x = test_x.drop(['isFraud'], axis=1)
train_x = train_x.values
test_x = test_x.values
print(train_x.shape)

nb_epoch = 100
batch_size = 32
input_dim = train_x.shape[1]
encoding_dim = 14
hidden_dim = int(encoding_dim/2)
learning_rate = 1e-7

input_layer = Input(shape=(input_dim, ))
encoder = Dense(encoding_dim, activation="sigmoid", activity_regularizer=regularizers.l1(learning_rate))(input_layer)
encoder = Dense(hidden_dim, activation="relu")(encoder)
decoder = Dense(hidden_dim, activation='sigmoid')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(metrics=['accuracy'],
                    loss='mean_squared_error',
                    optimizer='adam')

cp = ModelCheckpoint(filepath="autoencoder_fraud.h5",
                     save_best_only=True,
                     verbose=0)


tb = TensorBoard(log_dir='./logs',
                 histogram_freq=0,
                 write_graph=True,
                 write_images=True)

history = autoencoder.fit(train_x, train_x,
                          epochs=nb_epoch,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(test_x, test_x),
                          verbose=1,
                          callbacks=[cp, tb]).history

autoencoder = load_model('autoencoder_fraud.h5')
LABELS = ["Normal", "Fraud"]
predictions = autoencoder.predict(test_x)
mse = np.mean(np.power(test_x - predictions, 2), axis=1)
error_df = pd.DataFrame({'reconstruction_error': mse,
                         'true_class': test_y})
y_pred = [1 if e > 2.9 else 0 for e in error_df.reconstruction_error.values]
conf_matrix = confusion_matrix(error_df.true_class, y_pred)

print(classification_report(test_y, y_pred))

plt.plot(history['loss'], linewidth=2, label='Train')
plt.plot(history['val_loss'], linewidth=2, label='Test')
plt.legend(loc='upper right')
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
# plt.ylim(ymin=0.70,ymax=1)
plt.show()

plt.figure(figsize=(12,12))
sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d");
plt.title("Confusion Matrix")
plt.ylabel('True Class')
plt.xlabel('Predicted Class')
plt.show()
