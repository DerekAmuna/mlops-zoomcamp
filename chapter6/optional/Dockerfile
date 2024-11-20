FROM public.ecr.aws/lambda/python:3.11

# RUN pip install -U pip
# RUN pip install pipenv

RUN python -m pip install -U pip
RUN python -m pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "lambda_function.py", "model.py", "./" ]

CMD [ "lambda_function.lambda_handler" ]