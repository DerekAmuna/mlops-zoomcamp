FROM --platform=linux/amd64 amazon/aws-lambda-python:3.13
#public.ecr.aws/lambda/python:3.13

RUN pip install -U pip
RUN pip install pipenv


COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy 

COPY ["./lambda_function.py","../../model.py", "./"]
 
CMD ["lambda_function.lambda_handler"]