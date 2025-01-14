#!/bin/bash

# Get the run ID from SSM parameter store
RUN_ID=$(aws ssm get-parameter --name "/project/run_id" --query "Parameter.Value" --output text)
echo "Run ID to copy: $RUN_ID"

# Source and destination paths
SOURCE_BUCKET="mlflow-wine-quality-experiments"
DEST_BUCKET="wine-model"
SOURCE_PATH="1/${RUN_ID}/artifacts/model"
DEST_PATH="1/${RUN_ID}/artifacts/model"

# Copy the model directory
echo "Copying model from s3://${SOURCE_BUCKET}/${SOURCE_PATH}/ to s3://${DEST_BUCKET}/${DEST_PATH}/"
aws s3 cp "s3://${SOURCE_BUCKET}/${SOURCE_PATH}/" "s3://${DEST_BUCKET}/${DEST_PATH}/" --recursive

# Check if copy was successful
if [ $? -eq 0 ]; then
    echo "Successfully copied model to production bucket"
else
    echo "Error copying model to production bucket"
    exit 1
fi

