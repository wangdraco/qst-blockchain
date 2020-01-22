# import the necessary packages

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import LabelBinarizer,MultiLabelBinarizer
from sklearn.preprocessing import MinMaxScaler


inputPath = 'HousesInfo.txt'

cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
df = pd.read_csv(inputPath, sep=" ", header=None, names=cols)

print(df.head())
print(df.shape)
print('\n')
print(df.describe())
print('\n')
# determine (1) the unique zip codes and (2) the number of data
# points with each zip code
zipcodes = df["zipcode"].value_counts().keys().tolist()
counts = df["zipcode"].value_counts().tolist()
print(f'zipcodes = {zipcodes}, and counts = {counts}')

# loop over each of the unique zip codes and their corresponding
# count
for (zipcode, count) in zip(zipcodes, counts):
# the zip code counts for our housing dataset is *extremely*
# unbalanced (some only having 1 or 2 houses per zip code)
# so let's sanitize our data by removing any houses with less
# than 25 houses per zip code
        if count < 25:
                idxs = df[df["zipcode"] == zipcode].index
                df.drop(idxs, inplace=True)



print("[INFO] constructing training/testing split...")
(train, test) = train_test_split(df, test_size=0.25, random_state=42)
print('before max ix ',train[:])

maxPrice = train["price"].max()
trainY = train["price"] / maxPrice
testY = test["price"] / maxPrice
print('trainY = ',trainY[:])


continuous = ["bedrooms", "bathrooms", "area"]


cs = MinMaxScaler()
print('train[continuous] .shape is =',cs.fit(train[continuous]))
trainContinuous = cs.fit_transform(train[continuous])
testContinuous = cs.transform(test[continuous])
print('trainContinuus====',trainContinuous[:10])
print('\n and shape is ==',trainContinuous.shape)

print('testContinuus====',testContinuous.shape)

print('\n')
_ttt = np.array([[1, 2, 3, 4],
       [5, 6, 4, 8]])

_test = MultiLabelBinarizer().fit_transform((_ttt))
#print('_test is ',_test.classes_)
print('_test is ',_test)
print('\n')

print('before Lable Binarizer df["zipcode"] =',df["zipcode"])
zipBinarizer = LabelBinarizer().fit(df["zipcode"])
print('\n')
print('after label binarizer zipBinarizer ==',zipBinarizer.classes_,
      ' type is =',zipBinarizer)
print('\n train zipcode is ==',train["zipcode"])
trainCategorical = zipBinarizer.transform(train["zipcode"])
print('\n')
print('trainCategorical .data ==',trainCategorical,'\n')

print('trainCategorical .shape ==',trainCategorical.shape)
testCategorical = zipBinarizer.transform(test["zipcode"])
trainX = np.hstack([trainCategorical, trainContinuous])
testX = np.hstack([testCategorical, testContinuous])
print('---------------------------------------------\n',trainX.shape)

print(trainX)



