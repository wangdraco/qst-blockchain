from keras.datasets import boston_housing
(X_train, y_train), (X_test, y_test) = boston_housing.load_data()

print(X_train[0], y_train[0])
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# first we fit the scaler on the training dataset
scaler.fit(X_train)

# then we call the transform method to scale both the training and testing data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# a sample output
print(X_train_scaled[0])

from tensorflow.keras import models, layers
model = models.Sequential()

model.add(layers.Dense(8, activation='relu', input_shape=[X_train.shape[1]]))
model.add(layers.Dense(16, activation='relu'))

# output layer
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=100)

model.evaluate(X_test_scaled, y_test)

to_predict = X_train_scaled[:2]
# we call the predict method
predictions = model.predict(to_predict)
# print the predictions
print(predictions)
# output
# array([[13.272537], [39.808475]], dtype=float32)
# print the real values
print(y_train[:2])
# array([15.2, 42.3])