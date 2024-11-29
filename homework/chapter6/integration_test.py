#! /usr/bin/env python3
import pandas as pd
from datetime import datetime
import os
import boto3



def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)


try:
    s3_client.create_bucket(Bucket="nyc-duration")
except s3_client.exceptions.BucketAlreadyExists:
    pass


data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = [
    "PULocationID",
    "DOLocationID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]
options = {
    "client_kwargs": {
        "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": "us-east-1",
    }
}
df_input = pd.DataFrame(data, columns=columns)
input_file = "s3://nyc-duration/in/2023-01.parquet"
df_input.to_parquet(
    input_file, engine="pyarrow", compression=None, index=False, storage_options=options
)

response = s3_client.head_object(Bucket="nyc-duration", Key="in/2023/01.parquet")

file_size = response["ContentLength"]
print(f"File size: {file_size} bytes")

os.system("/usr/bin/python3 batch.py 2023 01")

output_file = "s3://nyc-duration/out/2023-01.parquet"
df_output = pd.read_parquet(output_file, storage_options=options)


prediction_sum = df_output["predictions"].sum()
print(f"Sum of predictions: {prediction_sum:.2f}")
