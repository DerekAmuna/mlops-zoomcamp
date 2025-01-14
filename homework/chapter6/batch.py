#!/usr/bin/env python
# coding: utf-8
import sys
import pickle
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_input_path(year, month):
    default_input_pattern = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"
    input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    print(input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = f"s3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet"
    output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)
    print(output_pattern)
    return output_pattern.format(year=year, month=month)


def read_data(filename, categorical):
    if filename.startswith("s3://"):
        options = {
            "client_kwargs": {
                "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
                "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "region_name": "us-east-1",
            }
        }
        df = pd.read_parquet(filename, storage_options=options)
    else:
        df = pd.read_parquet(filename)

    return prepare_data(df, categorical)


def prepare_data(df, categorical):
    df["duration"] = (
        df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    ).dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df[categorical] = df[categorical].fillna(-1).astype("str")
    return df


def main(year: int, month: int):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    categorical = ["PULocationID", "DOLocationID"]
    df = read_data(input_file, categorical)

    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    df_result = pd.DataFrame()
    df_result["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")
    df_result["predictions"] = y_pred

    df_result.to_parquet(output_file, engine="pyarrow", index=False)


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
