import json
import base64
import boto3
import os
import mlflow
import numpy as np


session = boto3.Session()
credentials = session.get_credentials()

# Access individual credentials
AWS_ACCESS_KEY_ID = credentials.access_key
AWS_SECRET_ACCESS_KEY = credentials.secret_key
AWS_REGION = session.region_name


os.environ['AWS_S3_ENDPOINT_URL'] = f'https://s3.{AWS_REGION}.amazonaws.com'

# MLflow setup
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

RUN_ID = "e308ab2a149249a4b161cb428b4abc23"

logged_model = f"s3://mlops-derek/1/{RUN_ID}/artifacts/model"
model = mlflow.pyfunc.load_model(logged_model)


PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_preds')
kinesis_client = boto3.client('kinesis', region_name=os.getenv('AWS_DEFAULT_REGION', AWS_REGION),
                             )

def predict(features):
    return model.predict(features)

predictions_event = []


def lambda_handler(event, context):
    for rec in event['Records']:
        encoded_data = rec['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        ride_event = json.loads(decoded_data)
        # print(f'Decode in JSON format:\n\n\n{ride_event}\n\n\n')
        

        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
        prediction = predict(ride)
        prediction = prediction.tolist() if isinstance(prediction, np.ndarray) else prediction
        prediction_event  =  {
            "model":"ride_duration_prediction_model",
            "version":RUN_ID,
            "prediction": {
                "ride_duration":prediction,
                "ride_id":ride_id
            }
        }
    
    
    kinesis_client.put_record(
            StreamName=PREDICTIONS_STREAM_NAME,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id)
    )

    predictions_event.append(prediction_event)

    return {
        "predictions":predictions_event
    }
