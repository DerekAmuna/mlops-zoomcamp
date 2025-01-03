FROM --platform=linux/amd64 amazon/aws-lambda-python:3.13
#public.ecr.aws/lambda/python:3.13

# RUN apt-get update && \
#     apt-get install -y \
#         build-essential \
#         python3-dev \
#         libatlas-base-dev \
#         gfortran \
#         pkg-config \
#         liblapack-dev \
#         libblas-dev && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pip install pipenv && \
  pipenv install --system --deploy

COPY ["lambda_function.py","model.py", "./"]
 
CMD ["lambda_function.lambda_handler"]