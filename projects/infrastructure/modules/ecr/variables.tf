variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "wine-quality-predictor"
}

variable "ecr_image_tag" {
  description = "Tag of the ECR image"
  type        = string
  default     = "latest"
}

variable "docker_image_local_path" {
  description = "Path to the Docker image"
  type        = string
}

variable "lambda_function_local_path" {
  description = "Path to the Lambda function"
  type        = string
}

variable "region" {
  description = "Region of the ECR repository"
  type        = string
  default     = "us-east-1"
}

variable "account_id" {
  description = "Account ID of the ECR repository"
  type        = string
}
