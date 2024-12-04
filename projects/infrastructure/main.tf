terraform {
  required_version = "1.9.8"
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = var.prod_bucket_name
}

# IAM role and policies
module "iam" {
  source = "./modules/iam"
  prod_model_bucket_arn = module.s3_bucket.prod_model_bucket_arn
  mlflow_bucket_arn = module.s3_bucket.mlflow_bucket_arn
  input_stream_arn = module.wine_input_stream.stream_arn
  output_stream_arn = module.wine_output_stream.stream_arn
  ecr_repository_arn = module.ecr.repository_arn
}

# kinesis input stream
module "wine_input_stream" {
  source = "./modules/kinesis"
  kinesis_stream_name = var.kinesis_input_stream_name
  kinesis_shard_count = var.kinesis_shard_count
}

module "wine_output_stream" {
  source = "./modules/kinesis"
  kinesis_stream_name = var.kinesis_output_stream_name
  kinesis_shard_count = var.kinesis_shard_count
}

module "ecr" {
  source = "./modules/ecr"
  ecr_repository_name = var.ecr_repository_name
  ecr_image_tag = "latest"
  lambda_function_local_path = "../lambda/lambda_function.py"
  docker_image_local_path = "../lambda/Dockerfile"
  account_id = data.aws_caller_identity.current.account_id
  region = var.aws_region
}

module "lambda" {
  source = "./modules/lambda"
  prod_bucket_name = var.prod_bucket_name
  output_stream_name = var.kinesis_output_stream_name
  lambda_role_arn = module.iam.lambda_role_arn
  image_uri = module.ecr.image_uri
  input_stream_arn = module.wine_input_stream.stream_arn
}

# Outputs
output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = var.prod_bucket_name
}

output "input_stream_name" {
  description = "Name of the Kinesis input stream"
  value       = var.kinesis_input_stream_name
}

output "output_stream_name" {
  description = "Name of the Kinesis output stream"
  value       = var.kinesis_output_stream_name
}

output "image_uri" {
  description = "URI of the ECR image"
  value       = module.ecr.image_uri
}
