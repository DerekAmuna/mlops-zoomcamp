#! /usr/bin/env bash

if [[ -z "${GITHUB_ACTIONS}" ]]; then
    cd "$(dirname "$0")"
fi

if [ -z "${LOCAL_IMAGE_NAME}" ]; then
    LOCAL_TAG=`date -I`
    export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set"
else
    echo "LOCAL_IMAGE_NAME is set to ${LOCAL_IMAGE_NAME}"
fi

docker build -t ${LOCAL_IMAGE_NAME} ..

docker compose up -d

sleep 2

pip install pipenv
pipenv run python test_docker.py

ERROR_CODE=$?

if [ $ERROR_CODE -ne 0 ]; then
    docker compose logs
fi

docker compose down
exit $ERROR_CODE
