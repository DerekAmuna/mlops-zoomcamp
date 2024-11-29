export S3_BUCKET_DEV=mlflow-derek
export S3_BUCKET_PROD=mlflow-derek-mlopszoomcamp
export PREDICTIONS_STREAM_NAME=ride_preds-mlopszoomcamp
export LAMBDA_FUNCTION_NAME=ride_pred_model_mlopszoomcamp
export RIDE_EVENTS_STREAM_NAME=ride_events-mlopszoomcamp

#for retrieving run_id from aws. Not recommended
export RUN_ID=$(aws s3 ls s3://${S3_BUCKET_DEV}/1/ | sort | tail -n 1 | awk -F'/' '{print $1}' | awk '{print $2}')

aws s3 sync s3://${S3_BUCKET_DEV}/ s3://${S3_BUCKET_PROD}

variables="{PREDICTIONS_STREAM_NAME=${PREDICTIONS_STREAM_NAME}, MODEL_BUCKET=${S3_BUCKET_PROD}, RUN_ID=${RUN_ID}}"

aws lambda update-function-configuration --function-name ${LAMBDA_FUNCTION_NAME} --environment "Variables=${variables}"