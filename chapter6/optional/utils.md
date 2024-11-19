Create S3 bucket for Terraform state

```zsh
aws s3api create-bucket --bucket tf-state-derek-mlops-zoomcamp
```

note the backend config file `backend.hcl`, otherwise, put all in that file in the `main.tf backend s3` portion
when using this method, terraform will be initialised as 

```zsh
terraform init \
    -backend-config=backend.hcl
```

make sure to specify all variables when running the apply command

all terraform variables if put in env file must be preceeded by `TF_VAR_`. if not will need the `-var` flag when running the apply command or will default to the value in the variables.tf file. 

```zsh
terraform apply \
  -var="source_stream_name=my-stream" \
  -var="project_id=project-123"
```

more robust way is to put them in a `terraform.tfvars` file

then you can just 

```zsh
terraform apply #or plan
```
or if different name used then 

```zsh
terraform apply -var-file=vars/dev.tfvars #or prod.tfvars
```

Check streams after running the apply command (also can check buckets, ecr or anything created at all through terraform)

```zsh
aws kinesis list-streams --endpoint-url ${AWS_ENDPOINT_URL}
```

``` zsh
export KINESIS_STREAM_INPUT=ride_events-mlops-zoomcamp
aws kinesis put-record \
--stream-name ${KINESIS_STREAM_INPUT} \
--partition-key 1 \
--cli-binary-format raw-in-base64-out \
--data '{"ride":{"PULocationID": 130, "DOLocationID": 205, "trip_distance": 3.66}, "ride_id": 459302002}'
```