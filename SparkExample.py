import pandas as pd





df = pd.DataFrame({'col1':['a','b','c','d'],
                   'col2':['d', 'g', 'f', 'e']})

#print(df['col1'].apply(cateToNumeric, args=[['a', 'b', 'c', 'd']]))


def cateToNumeric(item, order):
    return order.index(item)/(len(order)-1)

def columnCatToNum(col, order):
    return col.apply(cateToNumeric, args=[order])

def dfCatsToNums(df, colNameList, orderList):
    for i in range(len(colNameList)):
        df[colNameList[i]]=columnCatToNum(df[colNameList[i]], orderList[i])
    return df


orders = [['a', 'b', 'c', 'd'],
          ['d', 'e', 'f', 'g']]
cNames = ['col1', 'col2']
print(dfCatsToNums(df, cNames, orders))