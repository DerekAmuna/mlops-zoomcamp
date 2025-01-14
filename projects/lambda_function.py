import os
import model
import boto3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def init_model_service():
    # Determine environment
    is_test = os.getenv("TEST_RUN", "False").lower() == "true"
    logger.info(f"Environment: {'Test' if is_test else 'Production'}")

    try:
        if is_test:
            # Test configuration
            model_service = model.init(
                prediction_stream_name=os.getenv("PREDICTIONS_STREAM_NAME"),
                run_id=os.getenv("RUN_ID"),
                test_run=True
            )
        else:
            # Production configuration
            ssm = boto3.client('ssm')
            model_service = model.init(
                prediction_stream_name=ssm.get_parameter(Name='/project/predictions_stream_name')['Parameter']['Value'],
                run_id=ssm.get_parameter(Name='/project/run_id')['Parameter']['Value'],
                test_run=False
            )
        
        logger.info("Model service initialized successfully")
        return model_service

    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        raise

# Initialize model service when module loads
model_service = init_model_service()

def lambda_handler(event, context):
    preds = model_service.lambda_handler(event) 
    print(preds)
    return preds
