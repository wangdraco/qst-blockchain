from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, MaxPooling2D # Convolution2D=Conv2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense


from keras.preprocessing.image import ImageDataGenerator
import numpy as np

img_width = 150
img_height = 150
train_data_dir = 'data/train'
valid_data_dir = 'data/validation'
models_data_name = 'data/models/simple_CNN-20191006.h5'

train_datagen = ImageDataGenerator(
    rescale = 1./255,)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(
    rescale = 1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(directory=train_data_dir,
											   target_size=(img_width,img_height),
											   #classes=['dogs','cats'],
											   class_mode='binary',
                                               #class_mode='categorical',
											   batch_size=16)


validation_generator = test_datagen.flow_from_directory(directory=valid_data_dir,
											   target_size=(img_width,img_height),
											   #classes=['dogs','cats'],
											   class_mode='binary',
                                               #class_mode='categorical',
											   batch_size=32)




# step-2 : build model
#Sequential是多个网络层的线性堆叠
model =Sequential()

# input: 150x150 images with 3 channels -> (100, 100,3) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Convolution2D(32,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Convolution2D(32,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Convolution2D(64,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
#model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

print('model complied!!')

print('starting training....')
training = model.fit_generator(generator=train_generator, steps_per_epoch=2048 // 16,epochs=60,validation_data=validation_generator,validation_steps=832//16)

print('training finished!!')

print('saving weights to simple_CNN.h5')

#model.save_weights(models_data_name)
model.save(models_data_name)

print('all weights saved successfully !!')
#models.load_weights('models/simple_CNN.h5')


