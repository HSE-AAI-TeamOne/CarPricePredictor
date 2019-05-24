import os
import tensorflow as tf

from pathlib import Path

from flask import Flask, request, render_template, url_for
from flask_cors import CORS, cross_origin
from ki_adapter import load_model, make_prediction

# nur für development für spätere versionen entfernen
import logging
logger = logging.getLogger()

# model
model = load_model('models/custom_model.hdf5')
graph = tf.get_default_graph()


# server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    global model
    global graph
    logger.info("POST methode wurde erfolgreich aufgerufen")
    # gets the raw base64 string
    data_uri = request.form['data_uri']
    logger.info("data_uri wurde erfolgreich in variable geladen")

    prediction = make_prediction(model, graph, data_uri)

    return prediction


if __name__ == "__main__":
    app.run()
