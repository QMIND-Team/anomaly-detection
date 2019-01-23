from pyspark.mllib.regression import LabeledPoint
from numpy import array







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











def create_labeled_point(line_split):

    clean_line_split = line_split[0:41]

    try:
        clean_line_split[1] = protocols.index(clean_line_split[1])
    except:
        clean_line_split[1] = len(protocols)

        # convert service to numeric categorical variable
    try:
        clean_line_split[2] = services.index(clean_line_split[2])
    except:
        clean_line_split[2] = len(services)

        # convert flag to numeric categorical variable
    try:
        clean_line_split[3] = flags.index(clean_line_split[3])
    except:
        clean_line_split[3] = len(flags)

        # convert label to binary label
    attack = 1.0
    if line_split[41] == 'normal.':
        attack = 0.0

    return LabeledPoint(attack, array([float(x) for x in clean_line_split]))