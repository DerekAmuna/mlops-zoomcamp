#! /usr/bin/env python3

import os

import requests
from deepdiff import DeepDiff

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49657540666418930171109502259426480070896488208763191298",
                "data": "eyJyaWRlIjp7IlBVTG9jYXRpb25JRCI6IDEyMSwgIkRPTG9jYXRpb25JRCI6IDEzNSwgInRyaXBfZGlzdGFuY2UiOiAzLjYzNn0sICJyaWRlX2lkIjogNDU5NDQzNTU1NTMwMjAwMn0=",
                "approximateArrivalTimestamp": 1731198238.106,
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49657540666418930171109502259426480070896488208763191298",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::361769579073:role/lambda-kinesis-role",
            "awsRegion": "eu-north-1",
            "eventSourceARN": "arn:aws:kinesis:eu-north-1:361769579073:stream/mlops-zoomcamp",
        }
    ]
}

url = "http://localhost:8080/2015-03-31/functions/function/invocations"
actual_response = requests.post(url, json=event, timeout=10).json()

expected_response = {
    "predictions": [
        {
            "model": "ride_duration_prediction_model",  # added s for failure testing
            "version": os.getenv("RUN_ID"),
            "prediction": {
                "ride_duration": 16.671032528356427,
                "ride_id": 4594435555302002,
            },
        }
    ]
}

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff = {diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff
