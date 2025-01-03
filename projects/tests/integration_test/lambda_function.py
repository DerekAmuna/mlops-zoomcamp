import logging
import os

import dotenv

import model

dotenv.load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_model_service():
    # FORCE TEST MODE FOR LOCAL TESTING
    TEST_RUN = True  # Hardcode for now
    logger.info(f"TEST_RUN set to: {TEST_RUN}")

    try:
        # Always use environment variables in test mode
        model_service = model.init(
            prediction_stream_name=os.getenv("PREDICTIONS_STREAM_NAME"),
            run_id=os.getenv("RUN_ID"),
            test_run=True,
        )

        logger.info("Model service initialized successfully")
        return model_service

    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        raise


# Initialize model service when module loads
logger.info("Starting Lambda initialization...")
model_service = init_model_service()
logger.info("Lambda initialization complete")


def lambda_handler(event, context):
    return model_service.lambda_handler(event)
