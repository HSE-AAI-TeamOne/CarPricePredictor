import os
import tensorflow as tf

from pathlib import Path
from flask import Flask, request
from flask_cors import CORS, cross_origin
from ki_adapter import load_model, make_prediction


# model
model = load_model('models/custom_model.hdf5')
graph = tf.get_default_graph()

# server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['POST'])
@cross_origin()
def root():
    global model
    global graph
# path from js
    path = request.form['path']
    path = Path(path)
    path = path.absolute().as_posix()

    prediction = make_prediction(model, graph, path)

    if os.path.exists(path):
        os.remove(path)

    return prediction


if __name__ == "__main__":
    app.run()
