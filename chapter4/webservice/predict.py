# service without mlflow server
from flask import Flask, request, jsonify
import pickle
import mlflow
from mlflow.tracking import MlflowClient
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("duration-prediction")
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

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
logged_model = f"runs:/{RUN_ID}/model"
model = mlflow.pyfunc.load_model(logged_model)

dv = client.download_artifacts(run_id=RUN_ID, path="dv.bin")
with open(dv, "rb") as f_in:
    dv = pickle.load(f_in)

# with open("intro_lm.bin", "rb") as f_in:
#     dv, model = pickle.load(f_in)


def predict(features):
    X = dv.transform(features)
    y_pred = model.predict(X)
    return y_pred[0]


# from here is the flask app code
app = Flask("duration-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    # input features for ride
    ride = request.get_json()
    # predict the duration
    y_pred = predict(ride)
    # return the result
    result = {"duration": y_pred, "RUN_ID": RUN_ID}
    return jsonify(result)  # jsonify is used to convert the result to a json object


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)

# can be quite messy see cleaner version using predict2.py
