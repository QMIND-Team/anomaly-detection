import pandas as pd
import numpy as np
from scipy import stats
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
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
TEST_PCT = 0.2

df = pd.read_csv("C:\\Users\\Colin Cumming\\Desktop\\Qmind\\Training_Project\\InsuranceTest\\claim.csv", index_col="PolicyNumber")

columnNames = ['Month', 'WeekOfMonth', 'DayOfWeek', 'Make',
                    'AccidentArea', 'DayOfWeekClaimed', "MonthClaimed",
                    "WeekOfMonthClaimed", "Sex", "MaritalStatus", "Fault",
                    "PolicyType", "VehicleCategory", "VehiclePrice",
                    "RepNumber",
                    "Deductible", "DriverRating", "Days_Policy_Accident",
                    "Days_Policy_Claim", "PastNumberOfClaims", "AgeOfVehicle",
                    "AgeOfPolicyHolder", "PoliceReportFiled", "WitnessPresent",
                    "AgentType", "NumberOfSuppliments", "AddressChange_Claim",
                    "NumberOfCars", "Year", "BasePolicy"]

def oneHot(df, columnName):
    one_hot = pd.get_dummies(df[columnName])
    one_hot.columns = [columnName + ':' + str(x) for x in one_hot.columns]
    # Remove type column
    df = df.drop(columnName, axis=1)
    # Join the encoded df
    df = df.join(one_hot)
    return df

def multipleOneHot(df, columnNames):
    for name in columnNames:
        df = oneHot(df, name)
    # df['Age'] = StandardScaler().fit_transform(df['Age'].values.reshape(-1,1))
    df = df.drop(['Age'], axis=1)
    return df
#
# def importdata():
#
#     #converting all words into numbers
#
#     sex = pd.get_dummies(['Sex'])
#     sex.columns = ['Sex' + ':' + str(x) for x in sex.columns]
#     df.drop(['Sex'], axis=1)
#     df = df.join(sex)
#
#     month = pd.get_dummies(df['Month'])
#     df.drop(['Month'], axis=1)
#     df = df.join(month)
#
#     dayWeek = pd.get_dummies(df['DayOfWeek'])
#     df.drop(['DayOfWeek'], axis=1)
#     df = df.join(dayWeek)
#
#     make = pd.get_dummies(df['Make'])
#     df.drop(['Make'], axis=1)
#     df = df.join(make)
#
#     accidentArea = pd.get_dummies(df['AccidentArea'])
#     df.drop(['AccidentArea'], axis=1)
#     df = df.join(accidentArea)
#
#     dayClaimed = pd.get_dummies(df['DayOfWeekClaimed'])
#     dayClaimed.columns = ['DayOfWeekClaimed' + ':' + str(x) for x in dayClaimed.columns]
#     df.drop(['DayOfWeekClaimed'], axis=1)
#     df = df.join(dayClaimed)
#
#     monthClaim = pd.get_dummies(df['MonthClaimed'])
#     monthClaim.columns = ['MonthClaimed' + ':' + str(x) for x in monthClaim.columns]
#     df.drop(['MonthClaimed'], axis=1)
#     df = df.join(monthClaim)
#
#     maritalStat = pd.get_dummies(df['MaritalStatus'])
#     df.drop(['MaritalStatus'], axis=1)
#     df = df.join(maritalStat)
#
#     fault = pd.get_dummies(df['Fault'])
#     df.drop(['Fault'], axis=1)
#     df = df.join(fault)
#
#     vehicle = pd.get_dummies(df['VehicleCategory'])
#     df.drop(['VehicleCategory'], axis=1)
#     df = df.join(vehicle)
#
#     policy = pd.get_dummies(df['PolicyType'])
#     df.drop(['PolicyType'], axis=1)
#     df = df.join(policy)
#
#     price = pd.get_dummies(df['VehiclePrice'])
#     df.drop(['VehiclePrice'], axis=1)
#     df = df.join(price)
#
#     accident = pd.get_dummies(df['Days_Policy_Accident'])
#     df.drop(['Days_Policy_Accident'], axis=1)
#     df = df.join(accident)
#
#     claimDays = pd.get_dummies(df['Days_Policy_Claim'])
#     claimDays.columns = ['Days_Policy_Claim' + ':' + str(x) for x in claimDays.columns]
#     df.drop(['Days_Policy_Claim'], axis=1)
#     df = df.join(claimDays)
#
#     numberOfClaims = pd.get_dummies(df['PastNumberOfClaims'])
#     numberOfClaims.columns = ['PastNumberOfClaims' + ':' + str(x) for x in numberOfClaims.columns]
#     df.drop(['PastNumberOfClaims'], axis=1)
#     df = df.join(numberOfClaims)
#
#     ageOfVehicle = pd.get_dummies(df['AgeOfVehicle'])
#     df.drop(['AgeOfVehicle'], axis=1)
#     df = df.join(ageOfVehicle)
#
#     policyHolder = pd.get_dummies(df['AgeOfPolicyHolder'])
#     df.drop(['AgeOfPolicyHolder'], axis=1)
#     df = df.join(policyHolder)
#
#     reportFiled = pd.get_dummies(df['PoliceReportFiled'])
#     df.drop(['PoliceReportFiled'], axis=1)
#     df = df.join(reportFiled)
#
#     witness = pd.get_dummies(df['WitnessPresent'])
#     witness.columns = ['WitnessPresent' + ':' + str(x) for x in witness.columns]
#     df.drop(['WitnessPresent'], axis=1)
#     df = df.join(witness)
#
#     agentTypes = pd.get_dummies(df['AgentType'])
#     agentTypes.columns = ['AgentType' + ':' + str(x) for x in agentTypes.columns]
#     df.drop(['AgentType'], axis=1)
#     df = df.join(agentTypes)
#
#     suppliments = pd.get_dummies(df['NumberOfSuppliments'])
#     suppliments.columns = ['NumberOfSuppliments' + ':' + str(x) for x in suppliments.columns]
#     df.drop(['NumberOfSuppliments'], axis=1)
#     df = df.join(suppliments)
#
#     address = pd.get_dummies(df['AddressChange_Claim'])
#     df.drop(['AddressChange_Claim'], axis=1)
#     df = df.join(address)
#
#     numOfCars = pd.get_dummies(df['NumberOfCars'])
#     df.drop(['NumberOfCars'], axis=1)
#     df = df.join(numOfCars)
#
#     base = pd.get_dummies(df['BasePolicy'])
#     df.drop(['BasePolicy'], axis=1)
#     df = df.join(base)
#
#     year = pd.get_dummies(['Year'])
#     year.columns = ['Year' + ':' + str(x) for x in year.columns]
#     df.drop(['Year'], axis=1)
#     df = df.join(year)
#
#     print(df.shape)
#     print(df)
#     return df

def splitdataset(df):
    Y = df['FraudFound']
    df = df.drop('FraudFound', axis=1)
    X = df.copy()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=TEST_PCT, random_state=RANDOM_SEED)

    return X, Y, X_train, X_test, y_train, y_test

def train_using_gini(X_train, X_test, y_train):
        clf_gini = DecisionTreeClassifier(criterion = 'gini', splitter='random')
        clf_gini.fit(X_train, y_train)
        return clf_gini


# Function to make predictions
def prediction(X_test, clf_object):
    # Predicton on test with giniIndex
    y_pred = clf_object.predict(X_test)
    print("Predicted values:")
    print(y_pred)
    return y_pred


# Function to calculate accuracy
def cal_accuracy(y_test, y_pred):
    print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))

    print("Accuracy : ",
          accuracy_score(y_test, y_pred) * 100)

    print("Report : ",
          classification_report(y_test, y_pred))

def main():
    # Building Phase
    data = multipleOneHot(df, columnNames)
    print(data.shape)
    print(data)
    X, Y, X_train, X_test, y_train, y_test = splitdataset(data)
    clf_gini = train_using_gini(X_train, X_test, y_train)
    # Operational Phase
    print("Results Using Gini Index:")

    # Prediction using gini
    y_pred_gini = prediction(X_test, clf_gini)
    cal_accuracy(y_test, y_pred_gini)

# Calling main function
if __name__ == "__main__":
    main()
