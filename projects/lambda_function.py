import os
import model
import boto3

ssm = boto3.client('ssm')


RUN_ID = ssm.get_parameter(Name='/project/run_id')['Parameter']['Value']
PREDICTIONS_STREAM_NAME = ssm.get_parameter(Name='/project/prediction_stream_name')['Parameter']['Value']
MODEL_BUCKET = ssm.get_parameter(Name='/project/model_bucket')['Parameter']['Value']
TEST_RUN = os.getenv("TEST_RUN", "False") == "True"

model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    run_id=RUN_ID,
    test_run=TEST_RUN,
    # model_bucket=MODEL_BUCKET
)

def lambda_handler(event, context):
    # pylint: disable=unused-argument
    return model_service.lambda_handler(event)
