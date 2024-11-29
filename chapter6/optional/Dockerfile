# FROM public.ecr.aws/lambda/python:3.1

#fix for pip failure in action
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

RUN /var/lang/bin/python3.11 -m pip install -U pip
RUN /var/lang/bin/python3.11 -m pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "lambda_function.py", "model.py", "./" ]

CMD [ "lambda_function.lambda_handler" ]