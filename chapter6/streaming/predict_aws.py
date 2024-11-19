# service with mlflow server and model saved in mlflow server with pipeline
import os

import numpy as np
import mlflow
from flask import Flask, jsonify, request

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# mlflow.set_experiment("duration-prediction")


RUN_ID = os.getenv("RUN_ID")


logged_model = f"s3://mlops-derek/1/{RUN_ID}/artifacts/model"  # pylint: disable=invalid-name
model = mlflow.pyfunc.load_model(logged_model)


def predict(features):
    if not isinstance(features, dict):
        raise ValueError("Input features should be a dictionary")
    y_pred = model.predict([features])
    if isinstance(y_pred, np.ndarray):
        y_pred = y_pred.tolist()
    return y_pred[0]


# from here is the flask app code
app = Flask("duration-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    # input features for ride
    ride = request.get_json()
    print(ride)
    # predict the duration
    y_pred = predict(ride)
    # return the result
    result = {"duration": y_pred, "RUN_ID": RUN_ID}
    return jsonify(result)  # jsonify is used to convert the result to a json object


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
