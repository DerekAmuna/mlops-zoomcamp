terraform {
  required_version = ">= 1.9.8"
  backend "s3" {}
}

provider "aws" {
}

data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id 
}



module "source_wine_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  name = "${var.source_stream_name}"
  tags = var.project_id
}


module "output_wine_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  name = "${var.output_stream_name}"
  tags = var.project_id
}


module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket}"
}


module "ecr_image" {
   source = "./modules/ecr"
   ecr_repo_name = "${var.ecr_repo_name}"
   account_id = local.account_id
   lambda_function_local_path = var.lambda_function_local_path
   docker_image_local_path = var.docker_image_local_path
   region = var.region
}

module "lambda_function" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.image_uri
  ecr_image_resource = module.ecr_image.ecr_image_resource
  lambda_function_name = "${var.lambda_function_name}"
  model_bucket = module.s3_bucket.name
  output_stream_name = "${var.output_stream_name}"
  output_stream_arn = module.output_wine_stream.stream_arn
  source_stream_name = "${var.source_stream_name}"
  source_stream_arn = module.source_wine_stream.stream_arn
}

module "ssm_parameters" {
  source = "./modules/ssm"
  
  output_stream_name = var.output_stream_name
  mlflow_run_id = "1542fc238fef40ddae60538ed932c35b"
  model_bucket_name = var.model_bucket
  experiment_id = "1"  
}
output "lambda_function" {
  value     = "${var.lambda_function_name}"
}

output "model_bucket" {
  value = module.s3_bucket.name
}

output "predictions_stream_name" {
  value     = "${var.output_stream_name}"
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}"
}