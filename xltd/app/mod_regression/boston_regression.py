import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import Adam,SGD
from sklearn.metrics import mean_squared_error

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


def main():
    print("Loading entire 506-item dataset into memory")
    data_file = "E:\\study\\ai-dataset\\0718vsm_McCaffrey\\boston_mm_tab.txt"
    all_data = np.loadtxt(data_file, delimiter="\t", skiprows=0, dtype=np.float32)

    print("Splitting data into 90-10 train-test")
    n = len(all_data)  # number rows
    indices = np.arange(n)  # an array [0, 1, . . 505]
    np.random.shuffle(indices)  # by ref
    split_train = int(0.90 * n)  # number training items
    data_x = all_data[indices, :-1]  # all rows, skip last col
    data_y = all_data[indices, -1]  # all rows, just last col

    train_x = data_x[0:split_train, :]  # rows 0 to ntr-1, all cols
    train_y = data_y[0:split_train]  # items 0 to ntr-1
    test_x = data_x[split_train:n, :]
    test_y = data_y[split_train:n]

    model = Sequential()
    model.add(Dense(10, input_dim=13, activation="tanh"))
    # model.add(Dropout(0.5))
    model.add(Dense(10, activation="tanh"))
    # model.add(Dropout(0.5))
    model.add(Dense(1, activation=None))

    simple_sgd = SGD(lr=0.010)

    model.compile(optimizer=simple_sgd, loss='mean_squared_error', metrics=['mse'])

    print("\nStarting training")
    max_epochs = 1000
    h = model.fit(train_x, train_y, batch_size=1, epochs=max_epochs, verbose=1)  # use 1 or 2
    print("Training complete")

    acc = my_accuracy(model, train_x, train_y, 0.15)
    print("\nModel accuracy on train data = %0.2f%%" % acc)

    acc = my_accuracy(model, test_x, test_y, 0.15)
    print("Model accuracy on test data  = %0.2f%%" % acc)

    raw_inpt = np.array([[0.02731, 0.00, 7.070, 0, 0.4690,
                          6.4210, 78.90, 4.9671, 2, 242.0, 17.80, 396.90,
                          9.14]], dtype=np.float32)

    norm_inpt = np.array([[0.000236, 0.000000, 0.242302,
                           -1.000000, 0.172840, 0.547998, 0.782698, 0.348962,
                           0.043478, 0.104962, 0.553191, 1.000000, 0.204470]],dtype=np.float32)

    print("\nUsing model to make prediction")
    print("Raw input = ")
    my_print(raw_inpt[0], 10, 4, 5)
    print("\nNormalized input =")
    my_print(norm_inpt[0], 10, 4, 5)

    med_price = model.predict(norm_inpt)
    med_price[0, 0] *= 10000
    print("\nPredicted median price = ")
    print("$%0.2f" % med_price[0, 0])
    model.save('E:\\study\\ai-dataset\\0718vsm_McCaffrey\\boston_model.h5')

    print("\nEnd demo ")


if __name__ == "__main__":
    main()

