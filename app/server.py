import os
import tensorflow as tf

from pathlib import Path

from flask import Flask, request, render_template, url_for, make_response
from ki_adapter import load_model, make_prediction
# REVIEW brauchen wir überhaupt cross origin wenn wir den ganzen pfad als open markieren?
from flask_cors import CORS, cross_origin

# nur für development für spätere versionen entfernen
import logging
logger = logging.getLogger()

# model
model = load_model('models/custom_model.hdf5')
graph = tf.get_default_graph()


# server
app = Flask(__name__)
cors = CORS(app)
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def root():
    logger.info("TEMPLATE wird weiter geleitet")
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    global model
    global graph
    logger.info("POST methode wurde erfolgreich aufgerufen")
    # gets the raw base64 string
    logger.info(request.form.get("data_uri"))
    if request.form.get("data_uri"):
        data_uri = request.form['data_uri']
        logger.info("data_uri wurde erfolgreich in variable geladen")
        prediction = make_prediction(model, graph, data_uri)
        return prediction
    return "Es wurde kein valides Bild angegeben"


if __name__ == "__main__":
    app.run()
    app.debug
