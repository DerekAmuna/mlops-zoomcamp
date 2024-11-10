# service with mlflow server and model saved in mlflow server with pipeline
from flask import Flask, request, jsonify
import mlflow
import numpy as np


MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# mlflow.set_experiment("duration-prediction")



RUN_ID = "e308ab2a149249a4b161cb428b4abc23"


logged_model = f"s3://mlops-derek/1/{RUN_ID}/artifacts/model"
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
