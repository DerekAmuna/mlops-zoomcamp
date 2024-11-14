FROM public.ecr.aws/lambda/python:3.11

RUN pip install -U pip
RUN pip install pipenv

ENV MLFLOW_TRACKING_URI=http://127.0.0.1:5000

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy 

COPY ["lambda_function.py", "./"]

CMD ["lambda_function.lambda_handler"]