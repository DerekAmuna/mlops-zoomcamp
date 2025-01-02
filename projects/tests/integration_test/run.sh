#! /usr/bin/env bash
# if [[ -z "${GITHUB_ACTIONS}" ]]; then
#     cd "$(dirname "$0")"
# fi
# pwd

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

if [ -z "${LOCAL_IMAGE_NAME}" ]; then
    LOCAL_TAG=`date -I`
    export LOCAL_IMAGE_NAME="wine_quality:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set"
else
    echo "LOCAL_IMAGE_NAME is set to ${LOCAL_IMAGE_NAME}"
fi

if [ -z "${KINESIS_STREAM_NAME}" ]; then
    echo "KINESIS_STREAM_NAME is not set"
    export KINESIS_STREAM_NAME="wine_events"
else
    echo "KINESIS_STREAM_NAME is set to ${KINESIS_STREAM_NAME}"
fi

# docker build -t ${LOCAL_IMAGE_NAME} ..
docker build --pull -t ${LOCAL_IMAGE_NAME} ../..

docker compose -f docker-compose.yml up -d

sleep 5 #try 2 seconds if getting connection refused error



pip install pipenv

# pipenv run python test_docker.py

# ERROR_CODE=$?

# if [ $ERROR_CODE -ne 0 ]; then
#     docker compose logs
#     docker compose down
#     exit $ERROR_CODE
# fi
cd tests/integration_test
pipenv run python test_lambda.py

ERROR_CODE=$?

if [ $ERROR_CODE -ne 0 ]; then
    docker compose logs
    docker compose down
    exit $ERROR_CODE
fi

docker compose down