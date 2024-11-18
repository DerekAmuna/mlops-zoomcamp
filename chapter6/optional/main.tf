terraform {
  required_version = ">= 1.9.8"
  backend "s3" {}
}

provider "aws" {
  region = var.AWS_DEFAULT_REGION
  #config for localstack
  # access_key                  = "test"
  # secret_key                  = "test"
  # skip_credentials_validation = true
  # skip_metadata_api_check     = true
  # skip_requesting_account_id  = true
  # s3_use_path_style         = true  

  # endpoints {
  #   s3  = "http://localhost:4566"
  #   sts = "http://localhost:4566"
  #   iam  = "http://localhost:4566"
  #   lambda = "http://localhost:4566"
  #   kinesis = "http://localhost:4566"
  # }
}

data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id #can be account_id, arn, id, user_id
}


module "source_kinesis" {
  source = "./modules/kinesis"
  name = "${var.source_stream_name}-${var.project_id}"
  retention_period = 24
  shard_count = 1
  # shard_level_metrics = ["I comingBytes", "OutgoingBytes"] left out as all of default metrics are enabled
  tags = var.project_id

}


module "output_kinesis" {
  source = "./modules/kinesis"
  name = "${var.output_stream_name}-${var.project_id}"
  retention_period = 24
  shard_count = 1
  tags = var.project_id
}

module "model_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket_name}-${var.project_id}"

}

module "ecr_image" {
  source = "./modules/ecr"
  ecr_model_repo_name = "${var.ecr_model_repo_name}-${var.project_id}"
  image_tag = var.image_tag
  lambda_function_local_path = var.lambda_function_local_path
  docker_file_local_path = var.docker_file_local_path
  account_id = local.account_id
  region = var.AWS_DEFAULT_REGION
  # ecr_endpoint_url = var.ecr_endpoint_url
}

module "lambda_function" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.lambda_image_uri 
  function_name = var.function_name
  model_bucket = module.model_bucket.name
  output_stream_name = "${var.output_stream_name}-${var.project_id}"
  output_stream_arn = module.output_kinesis.stream_arn
  source_stream_name = "${var.source_stream_name}-${var.project_id}"
  source_stream_arn = module.source_kinesis.stream_arn

}