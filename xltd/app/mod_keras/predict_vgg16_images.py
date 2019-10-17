# -*- coding: UTF-8 -*-


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
#from keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import os
import numpy as np
from imutils import paths


base_dir = 'd:/keras-data'
model_dir = os.path.join(base_dir, 'models')
pred_dir = os.path.join(base_dir, 'prediction')

# grab all image paths in the input directory and randomly sample them
imagePaths = list(paths.list_images(pred_dir))
print('image is =====================',imagePaths)
#random.shuffle(imagePaths)
imagePaths = imagePaths[:16]

# initialize our list of results
results = []

# 【0】加载vgg16模型，加载预训练权重
model = load_model(model_dir+'/cats_and_dogs_pandas.h5')
#print(model.summary())                              # 打印模型概况
#plot_model(model,to_file = 'a simple convnet.png')  # 画出模型结构图，并保存成图片

# loop over our sampled image paths
for p in imagePaths:

    #using OpenCV processing........
    # load our original input image
    # orig = cv2.imread(p)

    # pre-process our image by converting it from BGR to RGB channel
    # ordering (since our Keras mdoel was trained on RGB ordering),
    # resize it to 150x150 pixels,same as models' pixels and then scale the pixel intensities
    # to the range [0, 1]
    # _image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    # _image = cv2.resize(_image, (150, 150))
    # _image = _image.astype("float") / 255.0

    # order channel dimensions (channels-first or channels-last)
    # depending on our Keras backend, then add a batch dimension to
    # the image
    # _image = image.img_to_array(_image)
    # _image = np.expand_dims(_image, axis=0)

    # make predictions on the input image
    # pred = model.predict(_image)
    # pred = pred.argmax(axis=1)[0]

    # an index of zero is the 'cat' label while an index of
    # one is the 'dog' label
    # label = "cat" if pred == 0 else "dog"
    # color = (0, 0, 255) if pred == 0 else (0, 255, 0)

    # resize our original input (so we can better visualize it) and
    # then draw the label on the image
    # orig = cv2.resize(orig, (128, 128))
    # cv2.putText(orig, label, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #             color, 2)

    # add the output image to our list of results
    #results.append(orig)

    #using Keras to process ......
    imag = image.load_img(p, target_size=(150, 150))
    imag = image.img_to_array(imag)
    imag = np.expand_dims(imag, axis=0)

    # make predictions on the input image
    pred = model.predict(imag)

    #model_structure = model.to_json()
    #print('model_structe is ++++++++++++++',model_structure)

    print('first model.predict(imag) is =====================,',pred, ' and pred.argmax(axis=1)=',pred.argmax(axis=1))
    pred = pred.argmax(axis=1)[0] #finds the index of the max value (the 0-th “cats” index).

    print('in the loop ,prediction is =',p,' value=',pred)



labels =['dog','cat','panda']
labels = np.array(labels)
print(labels)