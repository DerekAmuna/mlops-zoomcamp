#! /usr/bin/env python3
import lambda_function
import requests


event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49657540666418930171109502259426480070896488208763191298",
                "data": "eyJyaWRlIjp7IlBVTG9jYXRpb25JRCI6IDEzMCwgIkRPTG9jYXRpb25JRCI6IDIwNSwgInRyaXBfZGlzdGFuY2UiOiAzLjY2fSwgInJpZGVfaWQiOiA0NTkzMDIwMDJ9",
                "approximateArrivalTimestamp": 1731198238.106
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49657540666418930171109502259426480070896488208763191298",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::361769579073:role/lambda-kinesis-role",
            "awsRegion": "eu-north-1",
            "eventSourceARN": "arn:aws:kinesis:eu-north-1:361769579073:stream/mlops-zoomcamp"
        }
    ]
}

url = "http://localhost:8080/2015-03-31/functions/function/invocations"
response = requests.post(url, json=event)

# result = lambda_function.lambda_handler(event, None)
print(response.json())
