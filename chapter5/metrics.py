#! /usr/bin/env python

import datetime
import time
import random
import logging
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
    DatasetSummaryMetric,
)

from prefect import flow, task

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

SEND_TIMEOUT = 15
rand = random.Random()

# sql queries
create_table_query = """
DROP TABLE IF EXISTS drift_metrics;
CREATE TABLE IF NOT EXISTS drift_metrics (
    timestamp timestamp NOT NULL,
    prediction_drift float NOT NULL,
    num_drifted_columns integer NOT NULL,
    share_missing_values float NOT NULL
);
"""
# for keeping up metrics, the ref dat needs to be loaded with the model then
# the data is placed in buckets like daily or monthly yearly etc
# allows for calc of data drift
reference_data = pd.read_parquet("data/reference.parquet")
with open("models/lin_reg.bin", "rb") as f_in:
    model = joblib.load(f_in)

raw_data = pd.read_parquet("data/green_tripdata_2022-02.parquet")
begin = datetime.datetime(2022, 2, 1)

num_features = ["trip_distance"]
cat_features = ["PULocationID", "DOLocationID"]
target = ["duration"]

column_mapping = ColumnMapping(
    prediction="preds",
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None,
)

report = Report(
    metrics=[
        ColumnDriftMetric(column_name="preds"),
        DatasetMissingValuesMetric(),
        DatasetDriftMetric(),
        DatasetSummaryMetric(),
    ]
)


# connecrts to db.
@task
def prepare_db():
    with psycopg.connect(
        host="localhost",
        user="postgres",
        password="example",
        port=5432,
        autocommit=True,
    ) as conn:
        res = conn.execute(
            """
            SELECT 1 FROM pg_database WHERE datname ='test'
        """
        )
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE test;")
        with psycopg.connect(
            host="localhost",
            dbname="test",
            user="postgres",
            password="example",
            port=5432,
        ) as conn:
            conn.execute(create_table_query)


@task
def calculate_metrics_postgresql(curr, i=1):  # CURR is a cursor object
    current_data = raw_data[
        (raw_data["lpep_pickup_datetime"] >= (begin + datetime.timedelta(days=i)))
        & (raw_data["lpep_pickup_datetime"] < (begin + datetime.timedelta(days=i + 1)))
    ]

    current_data.fillna(0, inplace=True)
    current_data["preds"] = model.predict(current_data[num_features + cat_features])

    report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    result = report.as_dict()

    prediction_drift = result["metrics"][0]["result"]["drift_score"]
    num_drifted_columns = result["metrics"][2]["result"]["number_of_drifted_columns"]
    share_missing_values = result["metrics"][1]["result"]["current"][
        "share_of_missing_values"
    ]

    curr.execute(
        """
        INSERT INTO drift_metrics (timestamp, prediction_drift, num_drifted_columns, share_missing_values)
        VALUES (%s, %s, %s, %s)
        """,
        (
            begin + datetime.timedelta(days=i),
            prediction_drift,
            num_drifted_columns,
            share_missing_values,
        ),
    )


@flow
def batch_monitoring_backfill():
    prepare_db()
    last_send = datetime.datetime.now(pytz.utc) - datetime.timedelta(
        seconds=SEND_TIMEOUT
    )

    with psycopg.connect(
        host="localhost",
        dbname="test",
        user="postgres",
        password="example",
        port=5432,
        autocommit=True,
    ) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

            new_send = datetime.datetime.now(pytz.utc)
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send += datetime.timedelta(seconds=SEND_TIMEOUT)
            logging.info("data sent")


if __name__ == "__main__":
    batch_monitoring_backfill()
