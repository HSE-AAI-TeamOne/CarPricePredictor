from ki.resnet_152 import resnet152_model
from keras.utils import plot_model
import cv2 as cv
import numpy as np
import scipy.io
import tensorflow as tf
import pandas as pd
import base64

# nur für development für spätere versionen entfernen
import logging
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/backend.log", level=logging.DEBUG,
                    filemode="w", format=LOG_FORMAT)
logger = logging.getLogger()

# get cv image from data_uri


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    return img


def load_model(weights_path):
    img_width, img_height = 224, 224
    num_channels = 3
    num_classes = 196

    model = resnet152_model(img_height, img_width, num_channels, num_classes)
    model.load_weights(weights_path, by_name=True)
    return model

# geht jetzt mit img string


def make_prediction(model, graph, data_uri):
    # currently only gety data_uri
    img_width, img_height = 224, 224
    logger.info("make_prediction wurde aufgerufen")
    # ruft die funktion convert auf
    bgr_img = data_uri_to_cv2_img(data_uri)

    logger.info("wurde erfolgreich konvertiert")

    bgr_img = cv.resize(bgr_img, (img_width, img_height), cv.INTER_CUBIC)
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    rgb_img = np.expand_dims(rgb_img, 0)
    logger.info("image wurder erfolgreich geprocessed")
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
        car_price = "Kein Preis vorhanden"

    prob = round(prob*100, 2)

    return str(class_names)+"<br>" + str(prob) + "%" + "<br>" + car_price
