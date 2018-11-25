import pandas as pd
import numpy as np 
#%matplotlib inline 
from matplotlib import pyplot as plt
import os
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

#import matplotlib.lines as mlines
#from mpl_toolkits.mplot3d import Axes3D
#import seaborn as sns
#from sklearn.model_selection import train_test_split, learning_curve
#from sklearn.metrics import average_precision_score
#from xgboost.sklearn import xgbClassifier
#from xgboost import plot_importance, to_graphviz

#os.chdir('..')
#os.chdir('documents/Github/Projects/Anomaly-Detection')

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


# Importing datset
df = pd.read_csv('credit_card_data.csv')
print('test')
print(df.head())

#Changing the customers name into only integers
def cleanName(name):
    '''A function that replaces the C and M in the customer ID's 
    with a 1 for M and a 2 for C. '''
    name = name.replace("M", '1').replace("C", '2')
    return int(name)
df['nameOrig'] = df['nameOrig'].apply(cleanName)

#Changing type to discrete values using one-hot encoding
def changeType(type):
    '''A function that replaces [PAYMENT, CASH_OUT, TRANSFER, DEBIT] with
        with a binary values'''
    type = type.replace("TRANSFER", '00001').replace("PAYMENT", '00010').replace(
        "DEBIT", '00100').replace("CASH_OUT", '01000').replace("CASH_IN", '10000')
    return int(type)

df['type'] = df['type'].apply(changeType)

test, train = train_test_split(df, test_size = 0.5)

#Features used
features =[
       "step", 
       "amount", 
       "nameOrig", 
       "type",
       "oldbalanceOrg"
        ]

#Seapating the features 
X_train = train.loc[:,features].values
X_test = test.loc[:,features].values

#Separting the target
Y_train = train.loc[:,"isFraud"].values
Y_test = test.loc[:,"isFraud"].values


#Instantiating the classifier 
gnb = GaussianNB()

# Train Classifier 
gnb.fit(X_train,Y_train)

y_pred = gnb.predict(X_test)

print("Number of mislabeled points out of a total {} points: {}, performance {:05.2f}%"
      .format(
              X_test.shape[0],
              (Y_test != y_pred).sum(),
              100*(1-Y_test != y_pred).sum()/X_test.shape[0])
      )
     
print("Total Fraud Cases {}".format(np.count_nonzero(Y_test == 1)))
#Checking the actual accuracy of the model        
from sklearn.metrics import confusion_matrix
cfm = confusion_matrix(Y_test, y_pred)
print('Confusion Matrix:\n',cfm)

#Visualization of Confusion matrix
labels = ['Not Fraud', 'Fraud']
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cfm, cmap =plt.cm.Blues)
fig.colorbar(cax)
ax.set_xticklabels(['']+ labels)
ax.set_yticklabels(['']+ labels)
plt.xlabel('Predicted')
plt.ylabel('Expected')
plt.show()



#Checking other metrics of the model
from sklearn.metrics import classification_report
print(classification_report(Y_test,y_pred))

#print('Precision is ' + (cfm[0][0])/(cfm[0][0]+cfm[1][0]))

#from sklearn.metrics import precision_recall_curve