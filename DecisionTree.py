import pandas as pd
# from sklearn.metrics import confusion_matrix
# from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report
from sklearn import tree
import graphviz

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

def cateToNumeric(item, order):
    return order.index(item)/(len(order)-1)

def columnCatToNum(col, order):
    return col.apply(cateToNumeric, args=[order])

def dfCatsToNums(df, colNameList, orderList):
    for i in range(len(colNameList)):
        df[colNameList[i]]=columnCatToNum(df[colNameList[i]], orderList[i])
    return df



def normalizeColumns(df, colNames):
    for i in range(len(colNames)):
        df[colNames[i]] = (df[colNames[i]] - df[colNames[i]].min()) / (df[colNames[i]].max() - df[colNames[i]].min())
    return df


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
                    "PolicyType", "VehicleCategory",
                    "RepNumber",
                    "Deductible", "DriverRating",
                    "PoliceReportFiled", "WitnessPresent",
                    "AgentType",
                    "Year", "BasePolicy"]

columnsToNormalize = [
    'Age', 'Deductible'
]

columnsForCatConversion = ['VehiclePrice',
                           'Days_Policy_Accident', "Days_Policy_Claim",
                           "PastNumberOfClaims", "AgeOfVehicle",
                           "AgeOfPolicyHolder", "NumberOfSuppliments",
                           "AddressChange_Claim", "NumberOfCars",
                           ]

ordersForCatConversion = [
    ['less than 20000', '20000 to 29000', '30000 to 39000', '40000 to 59000', '60000 to 69000', 'more than 69000'],
    ['none', '1 to 7', '8 to 15', '15 to 30', 'more than 30'],
    ['none', '1 to 7', '8 to 15', '15 to 30', 'more than 30'],
    ['none', '1', '2 to 4', 'more than 4'],
    ['new', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', 'more than 7'],
    ['16 to 17', '18 to 20', '21 to 25', '26 to 30', '31 to 35', '36 to 40', '41 to 50', '51 to 65', 'over 65'],
    ['none', '1 to 2', '3 to 5', 'more than 5'],
    ['no change', '4 to 8 years', '2 to 3 years', '1 year', 'under 6 months'],
    ['1 vehicle', '2 vehicles', '3 to 4', '5 to 8', 'more than 8']

]

# drop the columns not selected for use
columnsToDrop = [x if (x not in columnsForOneHot and x not in columnsForCatConversion) else '' for x in allColumns]
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
x = dfCatsToNums(x, columnsForCatConversion, ordersForCatConversion)
# in progress: x = normalizeColumns(x, columnsToNormalize)


#print(x)
# print(x.shape)
# print(y.shape)
# print()

trainingX, testingX = splitData(x, 0.6)
trainingY, testingY = splitData(y, 0.6)

# print(trainingX.shape)
# print(trainingY.shape)
# print(testingX.shape)
# print(testingY.shape)

# args: max_depth, max_leaf_nodes,
model = tree.DecisionTreeClassifier(max_leaf_nodes=4)
model = model.fit(trainingX, trainingY)

predictions = model.predict(testingX)

print(classification_report(testingY, predictions))

dot_data = tree.export_graphviz(model, out_file=None)
graph = graphviz.Source(dot_data)

graph.render(filename='model-out.png', view=True)


