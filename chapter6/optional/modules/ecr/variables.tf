variable "ecr_model_repo_name" {
  type = string
}

variable "image_tag" {
  type = string
  description = "The tag of the image to be pushed to ECR"
  default = "latest"
}

variable "lambda_function_local_path" {
  type = string
  description = "The local path to the lambda function python file"
}

variable "docker_file_local_path" {
  type = string
  description = "The local path to the docker file"
}

# variable "ecr_endpoint_url" {
#   type = string
#   description = "The endpoint URL of the ECR registry"
#   default = "http://localhost:4566"
# }

variable "region" {
  type = string
  description = "The region of the ECR registry"
  default = "eu-north-1"
}

variable "account_id" {}
