# Variables
ENV_FILE := .env
include $(ENV_FILE)
export

# Terraform variables
TF_VARS := -var-file=vars/prod.tfvars


# Terraform commands with LocalStack configuration
init:
	terraform init -backend-config=backend-prod.hcl -reconfigure

plan: init
	terraform plan $(TF_VARS)

apply: init
	terraform apply $(TF_VARS) -auto-approve

destroy:
	terraform destroy $(TF_VARS) -auto-approve

create-bucket:
	aws s3api create-bucket \
    --bucket tf-state-derek-mlops-zoomcamp \
    --region ${AWS_DEFAULT_REGION} \
    --create-bucket-configuration LocationConstraint=${AWS_DEFAULT_REGION}

put-record:
	aws kinesis put-record \
	--stream-name ${KINESIS_STREAM_INPUT} \
	--partition-key 1 \
	--cli-binary-format raw-in-base64-out \
	--data  '{"ride":{"PULocationID": 130, "DOLocationID": 205, "trip_distance": 3.66}, "ride_id": 459302002}' 

# LocalStack specific commands
create-bucket-local:
	aws --endpoint-url=$(LOCALSTACK_ENDPOINT) s3 mb s3://tf-state

check-localstack:
	curl $(LOCALSTACK_ENDPOINT)/health

# List resources
list-buckets:
	aws --endpoint-url=$(LOCALSTACK_ENDPOINT) s3 ls

list-streams:
	aws --endpoint-url=$(LOCALSTACK_ENDPOINT) kinesis list-streams

# Full setup
setup: create-bucket init plan apply

# Cleanup everything
teardown: destroy clean