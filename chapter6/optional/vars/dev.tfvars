AWS_DEFAULT_REGION = "us-east-1"
region = "us-east-1"
source_stream_name = "ride_events"
output_stream_name = "ride_preds"
ecr_repo_name = "ride_pred-dev-model"
model_bucket = "mlflow-derek"
image_tag = "latest"
lambda_function_local_path = "lambda_function.py"
model_local_path = "model.py"
docker_image_local_path = "Dockerfile"
model_bucket_name = "prediction-models-dev"
lambda_function_name = "ride_pred_model"
