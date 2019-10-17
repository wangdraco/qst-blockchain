# import the necessary packages
from tensorflow.keras.models import load_model
import argparse
import pickle
import cv2

# load the input image and resize it to the target spatial dimensions
image = cv2.imread('data/cats_00010.jpg')
output = image.copy()
image = cv2.resize(image, (150, 150))

# scale the pixel values to [0, 1]
image = image.astype("float") / 255.0

# image = image.flatten()
# image = image.reshape((1, image.shape[0]))
image = image.reshape((1, image.shape[0], image.shape[1],
		image.shape[2]))

print("[INFO] loading network and label binarizer...")
model = load_model('data/models/cats_and_dogs.h5')

# make a prediction on the image
preds = model.predict(image,verbose=1)
print('finished-----------------',preds)