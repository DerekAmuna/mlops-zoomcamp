#! /bin/zsh

docker compose -f localstack.dockercompose.yml up -d

aws s3api create-bucket --bucket tf-state --endpoint-url ${AWS_ENDPOINT_URL} \
 --create-bucket-configuration LocationConstraint=${AWS_DEFAULT_REGION} 

sleep 1

terraform init -backend-config=backend.hcl

terraform apply -var-file=vars/dev.tfvars

docker compose -f localstack.dockercompose.yml down