# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

import os

def load_house_attributes(inputPath):
	# initialize the list of column names in the CSV file and then
	# load it using Pandas
	cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
	df = pd.read_csv(inputPath, sep=" ", header=None, names=cols)

	# determine (1) the unique zip codes and (2) the number of data
	# points with each zip code
	#确定唯一的邮政编码集，然后用每个唯一的邮政编码计算数据点的数量
	#df["zipcode"].value_counts() 返回的是一个dict，key=zipcode，value是counts
	zipcodes = df["zipcode"].value_counts().keys().tolist()
	counts = df["zipcode"].value_counts().tolist()

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

	# return the data frame
	return df

def process_house_attributes(df, train, test):
	# initialize the column names of the continuous data
	continuous = ["bedrooms", "bathrooms", "area"]

	#归一化处理
	# performin min-max scaling each continuous feature column to
	# the range [0, 1]
	#fina result trainContinuous=[[0.44444444 0.45454545 0.56262899].., ]],shape=(271, 3)
	cs = MinMaxScaler()
	trainContinuous = cs.fit_transform(train[continuous])
	testContinuous = cs.transform(test[continuous])

	
	#标签二值化
	#fit函数接收1D或2D数组,返回非重复的1D向量数据,类似groupby，
	#此处返回[91901 92276 92677 92880 93446 93510 94501],7个特征
	# one-hot encode the zip code categorical data (by definition of
	# one-hot encoing, all output features are now in the range [0, 1])	
	zipBinarizer = LabelBinarizer().fit(df["zipcode"])
	#print('after label binarizer zipBinarizer ==',zipBinarizer.classes_)

	#after transform,the result like [[0 0 1 0 0 0 0], [0 1 0 0 0 0 0],shape=（271,7）
	trainCategorical = zipBinarizer.transform(train["zipcode"])
	testCategorical = zipBinarizer.transform(test["zipcode"])

	
	#将分类特征和连续特征连接起来，构建训练和测试数据点
	#numpy的hstack函数是横向堆叠（向右）, 沿axis=1的轴
	#最终得到的trainX.shape = (271,10),就是trainCategorical的7个特征加上trainContinuous的3个特征
	# construct our training and testing data points by concatenating
	# the categorical features with the continuous features
	trainX = np.hstack([trainCategorical, trainContinuous])
	testX = np.hstack([testCategorical, testContinuous])

	# return the concatenated training and testing data
	return (trainX, testX)



