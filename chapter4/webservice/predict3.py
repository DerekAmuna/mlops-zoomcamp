# batch deployment
from flask import Flask, request, jsonify
import mlflow
import numpy as np


MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("duration-prediction")

# Get the latest run ID
experiment = mlflow.get_experiment_by_name("duration-prediction")
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"],
    max_results=1,
)

if len(runs) == 0:
    raise Exception("No runs found in the experiment")

RUN_ID = runs.iloc[0].run_id
print(f"Using Run ID: {RUN_ID}")

# Load model as a PyFuncModel.
# model_run_path = /Users/dna/mlops-zoomcamp/chapter4/webservice/mlflow_artifacts/1/3fb7008b16534ce4b61ea373d96ddf42/artifacts/model
# can use if mlflow server is down
logged_model = f"runs:/{RUN_ID}/model"
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
