
from tensorflow.keras.applications import VGG16
import os
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers




#I mentioned for doing feature extraction,
#which is much slower and more expensive, but which allows you to use data augmentation
#during training: extending the conv_base model and running it end to end on
#the inputs.

#Downloading data from https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5
#detailed at VGG16.py , at https://github.com/fchollet/deep-learning-models/blob/master/vgg16.py
#using base model to train small datasets ,refering the book  'Deep Learning with Python.pdf'
conv_base = VGG16(weights='imagenet',include_top=False,input_shape=(150, 150, 3))

#conv_base.summary()



base_dir = 'd:/keras-data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')
model_dir = os.path.join(base_dir, 'models')

#特征提取方法，暂时不用
'''
datagen = ImageDataGenerator(rescale=1./255)
batch_size = 20
def extract_features(directory, sample_count):
    features = np.zeros(shape=(sample_count, 4, 4, 512))
    labels = np.zeros(shape=(sample_count))
    generator = datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='binary')
    i = 0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size: (i + 1) * batch_size] = features_batch
        labels[i * batch_size: (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:
            break

    return features, labels

train_features, train_labels = extract_features(train_dir, 2000)
validation_features, validation_labels = extract_features(validation_dir, 1000)
test_features, test_labels = extract_features(test_dir, 1000)

train_features = np.reshape(train_features, (2000, 4 * 4 * 512))
validation_features = np.reshape(validation_features, (1000, 4 * 4 * 512))
test_features = np.reshape(test_features, (1000, 4 * 4 * 512))
'''

#原始的模型训练方法
#The model consists of three convolution blocks with a max pool layer in each of them.
# There's a fully connected layer with 512 units on top of it thatr is activated by a relu activation function.
# The model outputs class probabilities based on binary classification by the sigmoid activation function.
'''
model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(150, 150 ,3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])
'''


#基于原有的vgg16模型进行训练
model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))

#final dense layer must have the same size as the number of labels (2 in this case):
#如果class_mode='binary', 则layers.Dense(1,activation='sigmoid'), 如果class_mode='categorical',则 layers.Dense(2..activation='sigmoid'
#sigmoid用于二分类，softmax用于多分类，如果有三个classes且class_mode='categorical'，则layers.Dense(3..activation='softmax'
model.add(layers.Dense(3, activation='softmax'))

# initialize the training training data augmentation object
#augmented train data ,利用图形变换，增强训练数据，验证和测试数据就不用增强了
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(150, 150),
                                                    batch_size=20,
                                                    color_mode="rgb",
                                                    shuffle=True,
                                                    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(validation_dir,
                                                        target_size=(150, 150),
                                                        batch_size=20,
                                                        class_mode='categorical')


model.compile(loss='categorical_crossentropy',optimizer=optimizers.RMSprop(lr=2e-5),metrics=['acc'])
history = model.fit_generator(train_generator,
                              steps_per_epoch=100,
                              epochs=20,
                              validation_data=validation_generator,
                              validation_steps=50)

print('finished compling..................')


model.save(model_dir + '/cats_and_dogs_pandas.h5')