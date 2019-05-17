import cv2 as cv
import numpy as np
import scipy.io
import tensorflow as tf
import pandas as pd

from keras.utils import plot_model
from ki.resnet_152 import resnet152_model


def load_model(weights_path):
    img_width, img_height = 224, 224
    num_channels = 3
    num_classes = 196

    model = resnet152_model(img_height, img_width, num_channels, num_classes)
    model.load_weights(weights_path, by_name=True)
    return model


def make_prediction(model, graph, img_path):
    img_width, img_height = 224, 224

    bgr_img = cv.imread(img_path)
    bgr_img = cv.resize(bgr_img, (img_width, img_height), cv.INTER_CUBIC)
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    rgb_img = np.expand_dims(rgb_img, 0)

    with graph.as_default():
        preds = model.predict(rgb_img)

    prob = np.max(preds)
    class_id = np.argmax(preds)

    cars_meta = scipy.io.loadmat('devkit/cars_meta')
    class_names = cars_meta['class_names']
    class_names = np.transpose(class_names)
    class_names = class_names[class_id][0][0]
    class_names = class_names[:-4]

    cardata = pd.read_csv("data/carData.csv", sep=';')
    datarow = cardata[cardata.carModel == str(class_names).lstrip().rstrip()]

    car_price = ''
    if datarow.shape[0] > 0:
        car_price = str(datarow.iloc[0]["carPrice"]) + '$'
    else:
        car_price = "kein preis vohanden"

    prob = round(prob*100, 2)

    return str(class_names)+"<br>" + str(prob) + "%" + "<br>" + car_price
