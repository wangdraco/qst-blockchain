import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import Adam,SGD

from tensorflow.keras.models import load_model

def load_car_attributes(inputPath):
	#cols = ["age", "gender", "miles", "debt", "income", "sales"]
	#df.columns
    df = pd.read_csv(inputPath, sep=",")
    df2= df[df.debt>0]
    print("max - min = ",df2["sales"].max(),"-",df2["sales"].min())
    return df2

def my_print(arr, wid, cols, dec):
    fmt = "% " + str(wid) + "." + str(dec) + "f "
    for i in range(len(arr)):
        if i > 0 and i % cols == 0: print("")
        print(fmt % arr[i], end="")
    print("")

def my_accuracy(model, data_x, data_y, pct_close):
    correct = 0
    wrong = 0
    n = len(data_x)
    for i in range(n):
        predicted = model.predict(np.array([data_x[i]], dtype=np.float32) )  # [[ x ]]
        actual = data_y[i]
        if np.abs(predicted[0][0] - actual) < np.abs(pct_close * actual):
            correct += 1
        else:
            wrong += 1
    return (correct * 100.0) / (correct + wrong)


def process_data():
    # test
    all_data = load_car_attributes("E:/study/ai-dataset/cars.csv")  # np.loadtxt("E:/study/ai-dataset/cars.csv",  delimiter=",", skiprows=1)
    maxPrice = all_data["sales"].max()

    print('df2 is \n', all_data)
    data_x = np.array(all_data)[:, 0:5]
    print('x is ', data_x)

    scaler_x = MinMaxScaler()
    data_x = scaler_x.fit_transform(data_x)
    print('after scaller x ix ', data_x)

    #目标值除10000，进行数据缩放
    # data_y = np.array(all_data)[:, 5] / 10000

    #使用minmax缩放目标值
    scaler_y = MinMaxScaler()
    data_y = np.array(all_data)[:, 5]
    data_y = scaler_y.fit_transform(np.reshape(data_y, (-1,1)))
    print('y is ', data_y[:10])
    # print('y is ===',y)
    # data_y=np.reshape(data_y, (-1,1))
    # print('after reshape y is ',data_y)

    print("Splitting data into 90-10 train-test")
    n = len(all_data)  # number rows

    split_train = int(0.90 * n)

    train_x = data_x[0:split_train, :]  # rows 0 to ntr-1, all cols
    train_y = data_y[0:split_train]  # items 0 to ntr-1
    test_x = data_x[split_train:n, :]
    test_y = data_y[split_train:n]

    return (train_x,train_y,test_x,test_y,scaler_x,scaler_y)


def main():
    (train_x, train_y, test_x, test_y, scaler_x,scaler_y) = process_data()

    #create neural network 5-10-10-1
    model = Sequential()
    model.add(Dense(10, input_dim=5, activation="tanh"))
    # model.add(Dropout(0.5))
    model.add(Dense(10, activation="tanh"))
    # model.add(Dropout(0.5))
    model.add(Dense(1, activation=None))

    simple_sgd = SGD(lr=0.010)

    model.compile(optimizer=simple_sgd, loss='mean_squared_error', metrics=['mse'])

    print("\nStarting training")
    max_epochs = 1000

    #h = model.fit(train_x, train_y,validation_split=0.2,, batch_size=1, epochs=max_epochs, verbose=1)  # use 1 or 2
    h = model.fit(train_x, train_y,validation_data=(test_x, test_y), batch_size=1, epochs=max_epochs, verbose=1)  # use 1 or 2
    print("Training complete")

    acc = my_accuracy(model, train_x, train_y, 0.15)
    print("\nModel accuracy on train data = %0.2f%%" % acc)

    acc = my_accuracy(model, test_x, test_y, 0.15)
    print("Model accuracy on test data  = %0.2f%%" % acc)

    raw_inpt = np.array([[31, 1.00, 58, 41576, 6215]], dtype=np.float32)

    norm_inpt = np.array([[0.26829268, 1.000000, 0.55172414,
                           0.69554886, 0.52065008]],dtype=np.float32)

    print("\nUsing model to make prediction")
    print("Raw input = ")
    my_print(raw_inpt[0], 10, 4, 5)
    print("\nNormalized input =")
    my_print(norm_inpt[0], 10, 4, 5)

    med_price = model.predict(norm_inpt)
    med_price[0, 0] *= 10000
    print("\nPredicted median price = ")
    print("$%0.2f" % med_price[0, 0])
    model.save('E:\\study\\ai-dataset\\cars_model_new3.h5')

    print("\nEnd demo ")

def test_model():
    model = load_model('E:\\study\\ai-dataset\\cars_model_new3.h5')
    (train_x, train_y, test_x, test_y, scaler_x,scaler_y) = process_data()

    #plot the predicted value against the actual value
    #Black broken line is the predicted values and we can see that it encompasses most of the values
    y_pred = model.predict(test_x)
    fig, ax = plt.subplots()
    ax.scatter(test_y, y_pred)
    ax.plot([test_y.min(), test_y.max()], [test_y.min(), test_y.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()

    plt.plot(test_y, label="y-original")
    plt.plot(y_pred, label="y-predicted")
    plt.legend()
    plt.show()

    #
    diff = y_pred.flatten() - test_y
    percentDiff = (diff / test_y) * 100
    absPercentDiff = np.abs(percentDiff)

    # compute the mean and standard deviation of the absolute percentage
    # difference
    mean = np.mean(absPercentDiff)
    std = np.std(absPercentDiff)

    # finally, show some statistics on our model
    # locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))

    #predict single data
    Xnew = np.array([[33, 1, 37, 8066, 10218]])
    Xnew = scaler_x.transform(Xnew)
    print('after transfomr is ',Xnew)

    # make a prediction on the giving data
    preds = model.predict(Xnew, verbose=1)
    print('the preds value is ',preds,' and real value is ',scaler_y.inverse_transform(preds))



if __name__ == "__main__":
    # main()
    test_model()