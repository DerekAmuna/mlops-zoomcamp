# Variables
ENV_FILE := .env
include $(ENV_FILE)
export

# Terraform variables
TF_VARS := -var-file=vars/dev.tfvars

# LocalStack endpoint
LOCALSTACK_ENDPOINT := http://localhost:4566

# Terraform commands with LocalStack configuration
init:
	terraform init -backend-config=backend.hcl -migrate-state

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