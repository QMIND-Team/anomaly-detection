import pandas as pd
# from sklearn.metrics import confusion_matrix
# from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report

import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 2000)

colNamesTypes = {"Month": str,
                 "WeekOfMonth": int,
                 "DayOfWeek": str,
                 "Make": str,
                 "AccidentArea": str,
                 "DayOfWeekClaimed": str,
                 "MonthClaimed": str,
                 "WeekOfMonthClaimed": int,
                 "Sex": str,
                 "MaritalStatus": str,
                 "Age": int,
                 "Fault": str,
                 "PolicyType": str,
                 "VehicleCategory": str,
                 "VehiclePrice": str,
                 "FraudFound_P": int,
                 "PolicyNumber": int,
                 "RepNumber": int,
                 "Deductible": int,
                 "DriverRating": int,
                 "Days_Policy_Accident": str,
                 "Days_Policy_Claim": str,
                 "PastNumberOfClaims": str,
                 "AgeOfVehicle": str,
                 "AgeOfPolicyHolder": str,
                 "PoliceReportFiled": str,
                 "WitnessPresent": str,
                 "AgentType": str,
                 "NumberOfSuppliments": str,
                 "AddressChange_Claim": str,
                 "NumberOfCars": str,
                 "Year": str,
                 "BasePolicy": str}


def moNameToNum(mo):
    if mo == 'Jan':
        mo = 1
    elif mo == 'Feb':
        mo = 2
    elif mo == 'Mar':
        mo = 3
    elif mo == 'Apr':
        mo = 4
    elif mo == 'May':
        mo = 5
    elif mo == 'Jun':
        mo = 6
    elif mo == 'Jul':
        mo = 7
    elif mo == 'Aug':
        mo = 8
    elif mo == 'Sep':
        mo = 9
    elif mo == 'Oct':
        mo = 10
    elif mo == 'Nov':
        mo = 11
    elif mo == 'Dec':
        mo = 12
    return mo


def dayToNum(day):
    if day == 'Monday':
        day = 1
    elif day == 'Tuesday':
        day = 2
    elif day == 'Wednesday':
        day = 3
    elif day == 'Thursday':
        day = 4
    elif day == 'Friday':
        day = 5
    elif day == 'Saturday':
        day = 6
    elif day == 'Sunday':
        day = 7


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
    return df


def splitData(data, ratioOfTraining):
    firstChunkEnd = int(ratioOfTraining * len(data) // 1)
    chunk1 = data.loc[0:firstChunkEnd]
    chunk2 = data.loc[firstChunkEnd + 1:len(data)] # i just took out a -1, perhaps this is needed bc the index column.
    return chunk1, chunk2


# import the csv with the assigned daatatypes and use PolicyNumber as the index column
df = pd.read_csv(r"C:\Users\jaker\Documents\QMIND\claims.csv",
                 dtype=colNamesTypes,
                 index_col="PolicyNumber")

# df['Month'] = df['Month'].apply(moNameToNum)


targetColumn = "FraudFound_P"

allColumns = ['Month', 'WeekOfMonth', 'DayOfWeek', 'Make',
              'AccidentArea', 'DayOfWeekClaimed', "MonthClaimed",
              "WeekOfMonthClaimed", "Sex", "MaritalStatus", "Age", "Fault",
              "PolicyType", "VehicleCategory", "VehiclePrice", "RepNumber",
              "Deductible", "DriverRating", "Days_Policy_Accident",
              "Days_Policy_Claim", "PastNumberOfClaims", "AgeOfVehicle",
              "AgeOfPolicyHolder", "PoliceReportFiled", "WitnessPresent",
              "AgentType", "NumberOfSuppliments", "AddressChange_Claim",
              "NumberOfCars", "Year", "BasePolicy"]

columnsForOneHot = ['Month', 'WeekOfMonth', 'DayOfWeek', 'Make',
                    'AccidentArea', 'DayOfWeekClaimed', "MonthClaimed",
                    "WeekOfMonthClaimed", "Sex", "MaritalStatus", "Fault",
                    "PolicyType", "VehicleCategory", "VehiclePrice",
                    "RepNumber",
                    "Deductible", "DriverRating", "Days_Policy_Accident",
                    "Days_Policy_Claim", "PastNumberOfClaims", "AgeOfVehicle",
                    "AgeOfPolicyHolder", "PoliceReportFiled", "WitnessPresent",
                    "AgentType", "NumberOfSuppliments", "AddressChange_Claim",
                    "NumberOfCars", "Year", "BasePolicy"]

# drop the columns not selected for oneHot encoding
columnsToDrop = [x if x not in columnsForOneHot else '' for x in allColumns]
actualColumnsToDrop = []
for x in columnsToDrop:
    if x != '':
        actualColumnsToDrop.append(x)
df = df.drop(columns=actualColumnsToDrop)

# copy and drop the column saying if its fraud or not
y = df["FraudFound_P"]
df = df.drop("FraudFound_P", axis=1)

# apply all the onehot encoding
x = multipleOneHot(df.copy(), columnsForOneHot)

# print(x.shape)
# print(y.shape)
# print()

trainingX, testingX = splitData(x, 0.6)
trainingY, testingY = splitData(y, 0.6)

# print(trainingX.shape)
# print(trainingY.shape)
# print(testingX.shape)
# print(testingY.shape)

model = BernoulliNB()
model.fit(trainingX, trainingY)

predictions = model.predict(testingX)
print(classification_report(testingY, predictions))