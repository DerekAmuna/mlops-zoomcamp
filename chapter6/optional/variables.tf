variable "AWS_DEFAULT_REGION" {
  type = string
}

variable "project_id" {
  type = string
  default = "mlops-zoomcamp"
}

variable "source_stream_name" {
  type = string
}

variable "output_stream_name" {
  type = string
}

variable "model_bucket_name" {
  type = string
}

variable "ecr_model_repo_name" {
  type = string
}

variable "image_tag" {
  type = string
}

variable "lambda_function_local_path" {
  type = string
}

variable "docker_file_local_path" {
  type = string
}

# variable "ecr_endpoint_url" {
#   type = string
#   default = "http://localhost:4566"
# }

variable "function_name" {
  type = string
}