docker compose up -d

aws s3 --endpoint-url http://localhost:4566 mb nyc-duration

pip install pipenv

pipenv run python integration_test.py

docker compose down