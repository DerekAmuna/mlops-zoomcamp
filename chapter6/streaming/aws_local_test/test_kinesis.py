# pylint: disable=all

import os
import json
from pprint import pprint

import boto3
from deepdiff import DeepDiff

kinesis_endpoint = os.getenv('KINESIS_URL', "http://localhost:4566")

SHARD_ID = "shardId-000000000000"

try:
   kinesis_client = boto3.client(
       'kinesis',
       region_name='us-east-1',
       endpoint_url=kinesis_endpoint,  
       aws_access_key_id='test',  
       aws_secret_access_key='test'  
   )

   stream_name = os.getenv("PREDICTIONS_STREAM_NAME", "ride_preds")
   response = kinesis_client.describe_stream(StreamName=stream_name)
except:
    print("Stream does not exist")

shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName=stream_name,
    ShardId=SHARD_ID,
    ShardIteratorType="TRIM_HORIZON",
)

shard_iterator_id = shard_iterator_response["ShardIterator"]


records_response = kinesis_client.get_records(
    ShardIterator=shard_iterator_id,
    Limit=1,
)


records = records_response["Records"]
pprint(records)


assert len(records) == 1


actual_record = json.loads(records[0]["Data"])
pprint(actual_record)

expected_record = {
    "model": "ride_duration_prediction_model",  # added s for failure testing
    "version": "e308ab2a149249a4b161cb428b4abc23",
    "prediction": {
        "ride_duration": 20.970334029909353,
        "ride_id": 4594435555302002,
    },
}

diff = DeepDiff(actual_record, expected_record, significant_digits=1)
print(f"diff={diff}")

assert "values_changed" not in diff
assert "type_changes" not in diff
