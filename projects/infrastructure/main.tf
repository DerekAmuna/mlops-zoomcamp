terraform {
  required_version = "1.9.8"
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

module "mlflow_s3" {
  source = "./modules/s3"
  bucket_name = var.mlflow_bucket_name
} 
