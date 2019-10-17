# -*- coding: UTF-8 -*-
#使用公开的训练好的模型进行图像识别，
#利用ResNet50网络进行ImageNet分类,源代码参考 E:\study\CV&DeepLearning\deep-learning-models-0.8
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os
import tensorflow as tf
os.environ["CUDA_VISIBLE_DEVICES"] = "6"

from keras.utils import plot_model
from matplotlib import pyplot as plt

# 【0】ResNet50模型，加载预训练权重
model = ResNet50(weights='imagenet')
print(model.summary())                              # 打印模型概况
#plot_model(model,to_file = 'a simple convnet.png')  # 画出模型结构图，并保存成图片

# 【1】从网上下载一张图片，保存在当前路径下
img_path = './data/tadiao.jpg'
img = image.load_img(img_path, target_size=(224, 224))

# 【2】显示图片
plt.imshow(img)
plt.show()

#【3】将图片转化为4d tensor形式
x = image.img_to_array(img)
print(x.shape) #(224, 224, 3)
x = np.expand_dims(x, axis=0)
print(x.shape) #(1, 224, 224, 3)

# 【4】数据预处理
"""
def preprocess_input(x, data_format=None, mode='caffe'):
   Preprocesses a tensor or Numpy array encoding a batch of images.

    # Arguments
        x: Input Numpy or symbolic tensor, 3D or 4D.
        data_format: Data format of the image tensor/array.
        mode: One of "caffe", "tf".
            - caffe: will convert the images from RGB to BGR,
                then will zero-center each color channel with
                respect to the ImageNet dataset,
                without scaling.
            - tf: will scale pixels between -1 and 1,
                sample-wise.

    # Returns
        Preprocessed tensor or Numpy array.

    # Raises
        ValueError: In case of unknown `data_format` argument.
"""
x = preprocess_input(x) #去均值中心化，preprocess_input函数详细功能见注释

# 【5】测试数据
preds = model.predict(x)
print(preds.shape)  # (1,1000)

# 【6】将测试结果解码为如下形式：
# [(class1, description1, prob1),(class2, description2, prob2)...]
print('Predicted:', decode_predictions(preds, top=3)[0])