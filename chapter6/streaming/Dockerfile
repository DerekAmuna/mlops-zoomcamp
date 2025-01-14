FROM public.ecr.aws/lambda/python:3.11.2024.11.22.15

#use if pulling from aws
# FROM localhost:4566/lambda/python:3.11 #use if pulling from localstack
# FROM --platform=amd64 python:3.11-slim

RUN pip install -U pip
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["lambda_function.py", "model.py","./"]

CMD ["lambda_function.lambda_handler"]
