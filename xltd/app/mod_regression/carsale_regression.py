from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


def load_car_attributes(inputPath):
	#cols = ["age", "gender", "miles", "debt", "income", "sales"]
	#df.columns
    df = pd.read_csv(inputPath, sep=",")
    df2= df[df.debt>0]
    print("max - min = ",df2["sales"].max(),"-",df2["sales"].min())
    return df2


def process_car_attributes(df, train, test):
    continuous = ["age", "gender", "miles", "debt", "income"]
    cs = MinMaxScaler()
    trainContinuous = cs.fit_transform(train[continuous])
    testContinuous = cs.transform(test[continuous])

    trainX =  np.array(trainContinuous)
    testX = np.array(testContinuous)

    test_new = np.array([[36, 0, 45, 13251, 10961]])
    test_new = cs.transform(test_new)
    print('in the mehtod test_new is ',test_new)

    return (trainX, testX, cs)

def create_mlp(dim, regress=False):
	# define our MLP network
	model = Sequential()
	model.add(Dense(32, input_dim=dim, activation="relu"))
	model.add(Dropout(0.5))
	model.add(Dense(16, activation="relu"))
	model.add(Dropout(0.5))

	# check to see if the regression node should be added
	if regress:
		model.add(Dense(1, activation="linear"))

	# return our model
	return model


df = load_car_attributes('E:/study/ai-dataset/cars.csv')

print("[INFO] constructing training/testing split...")
(train, test) = train_test_split(df, test_size=0.25, random_state=42)

# find the largest house price in the training set and use it to
# scale our house prices to the range [0, 1] (this will lead to
# better training and convergence)

maxPrice = train["sales"].max()
trainY = train["sales"] / maxPrice
testY = test["sales"] / maxPrice


print(f'trainY shape = {np.array(trainY).shape}')

trainY = np.array(trainY)
testY = np.array(testY)

# process the house attributes data by performing min-max scaling
# on continuous features, one-hot encoding on categorical features,
# and then finally concatenating them together
print("[INFO] processing data...")
(trainX, testX, cs) = process_car_attributes(df, train, test)
print(f'trainX shape = {trainX.shape}')

model = create_mlp(trainX.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
# model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

# train the model
print("[INFO] training model...")
model.fit(trainX, trainY, validation_data=(testX, testY),epochs=200, batch_size=10)

# make predictions on the testing data
print("[INFO] predicting house prices...")
preds = model.predict(testX)

print('final predict testX is ',testX[-1])
print(' and testY is ',testY[-1])

print(np.sqrt(mean_squared_error(testY,preds)))
pred_train= model.predict(trainX)
print(np.sqrt(mean_squared_error(trainY,pred_train)))



# compute the difference between the *predicted* house prices and the
# *actual* house prices, then compute the percentage difference and
# the absolute percentage difference
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)

# compute the mean and standard deviation of the absolute percentage
# difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)

# finally, show some statistics on our model
#locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("[INFO] avg. sales price: {}, std sales price: {}".format(df["sales"].mean(),df["sales"].std()))
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))

# scaler_x = MinMaxScaler()
# scaler_y = MinMaxScaler()
Xnew = np.array([[36, 0, 45, 13251, 10961]])
Xnew = cs.transform(Xnew)
#Xnew = np.array([[0.41463415,0.,0.40229885,0.22156961,0.91823741]])
print('after Xnew transformed is ',Xnew)
ynew= model.predict(Xnew)
print('result ynew is ==',ynew)
print('and trainY is ', trainY)
#test
# df2 = load_car_attributes("E:/study/ai-dataset/cars.csv") #np.loadtxt("E:/study/ai-dataset/cars.csv",  delimiter=",", skiprows=1)
# print('df2 is \n',df2)
# y=np.array(df2)[:,5]
# print('y is ===',y)
# y=np.reshape(y, (-1,1))
# cs.fit_transform(y)

#scaler_y.fit_transform(ynew)
# print('\n after transform ynew result is ==',ynew)
# print("\n MinMaxScaler ynew is ",cs.inverse_transform(ynew))
print('transfrom from max is ',ynew*maxPrice)

fig, ax = plt.subplots()
ax.scatter(testY, preds)
ax.plot([testY.min(), testY.max()], [testY.min(), testY.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
