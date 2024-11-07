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

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

SEND_TIMEOUT = 15
rand = random.Random()

# sql queries
create_table_query = """
DROP TABLE IF EXISTS metrics;
CREATE TABLE IF NOT EXISTS metrics (
    timestamp timestamp NOT NULL,
    value1 float NOT NULL,
    value2 varchar NOT NULL,
    value3 integer NOT NULL
);
"""

# getting the database up and running. practically the same as what the docker
# compose does


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


def calculate_metrics_postgresql(curr):  # CURR is a cursor object
    value1 = rand.randint(0, 1000)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    curr.execute(
        """
        INSERT INTO metrics (timestamp, value1, value2, value3)
        VALUES (%s, %s, %s, %s)
    """, # inputtinf the timexone, and values as strings
        (datetime.datetime.now(pytz.utc), value1, value2, value3)
    )

def main():
    prepare_db()
    last_send = datetime.datetime.now(pytz.utc) - datetime.timedelta(seconds=SEND_TIMEOUT)

    with psycopg.connect(
        host="localhost", dbname="test", user="postgres", password="example", port=5432, autocommit=True
    ) as conn:
        for i in range(0,100):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr)
            
            new_send = datetime.datetime.now(pytz.utc)
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send += datetime.timedelta(seconds=SEND_TIMEOUT)
            logging.info('data sent')

if __name__ == "__main__":
    main()