#! /usr/bin/env bash

cd "$(dirname "$0")"

LOCAL_TAG=$(date -I)
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"


docker build -t ${LOCAL_IMAGE_NAME} ..

docker compose up -d

sleep 1 #try 2 seconds if getting connection refused error

aws --endpoint-url=${AWS_ENDPOINT_URL} kinesis create-stream \
 --stream-name ${PREDICTIONS_STREAM_NAME} --shard-count 1

pipenv run python test_docker.py

ERROR_CODE=$?

if [ $ERROR_CODE -ne 0 ]; then
    docker compose logs
    docker compose down
    exit $ERROR_CODE
fi

pipenv run python test_kinesis.py

ERROR_CODE=$?

if [ $ERROR_CODE -ne 0 ]; then
    docker compose logs
    docker compose down
    exit $ERROR_CODE
fi

docker compose down
