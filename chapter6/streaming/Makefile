LOCAL_TAG:=$(shell date -I) #note the :
# LOCAL_IMAGE_NAME=stream-model-duration:${LOCAL_TAG}
include aws_local_test/.env


test1:
	@echo "KINESIS_STREAM_NAME: ${KINESIS_STREAM_NAME}"



test:
	pytest tests/

quality-check:
	isort .
	black .
	pylint --recursive=y .

build: quality-check test 
	@echo ${LOCAL_IMAGE_NAME}
	docker build -t ${LOCAL_IMAGE_NAME} .


integration-test: build 
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} ./integration-test/run.sh 

aws_local_test: build
	bash aws_local_test/run.sh

publish: build