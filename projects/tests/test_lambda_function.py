# projects/test_lambda_function.py
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_function.boto3.client')
    @patch('lambda_function.model.init')
    def test_lambda_handler(self, mock_model_init, mock_boto3_client):
        # Mock SSM parameters
        mock_ssm = MagicMock()
        mock_ssm.get_parameter.side_effect = lambda Name: {
            '/project/run_id': {'Parameter': {'Value': 'test_run_id'}},
            '/project/prediction_stream_name': {'Parameter': {'Value': 'test_prediction_stream_name'}},
            '/project/model_bucket': {'Parameter': {'Value': 'test_model_bucket'}}
        }[Name]
        mock_boto3_client.return_value = mock_ssm

        # Mock model service
        mock_model_service = MagicMock()
        mock_model_service.lambda_handler.return_value = {'statusCode': 200, 'body': 'Success'}
        mock_model_init.return_value = mock_model_service

        # Define a sample event
        event = {
            "Records": [
                {
                    "kinesis": {
                        "kinesisSchemaVersion": "1.0",
                        "partitionKey": "1",
                        "sequenceNumber": "49657540666418930171109502259426480070896488208763191298",
                        "data": "eyJyaWRlIjp7IlBVTG9jYXRpb25JRCI6IDEyMSwgIkRPTG9jYXRpb25JRCI6IDEzNSwgInRyaXBfZGlzdGFuY2UiOiAzLjYzNn0sICJyaWRlX2lkIjogNDU5NDQzNTU1NTMwMjAwMn0=",
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

        # Call the lambda_handler function
        response = lambda_handler(event, None)

        # Assertions
        mock_boto3_client.assert_called_once_with('ssm')
        mock_model_init.assert_called_once_with(
            prediction_stream_name='test_prediction_stream_name',
            run_id='test_run_id',
            test_run=False
        )
        mock_model_service.lambda_handler.assert_called_once_with(event)
        self.assertEqual(response, {'statusCode': 200, 'body': 'Success'})

if __name__ == '__main__':
    unittest.main()