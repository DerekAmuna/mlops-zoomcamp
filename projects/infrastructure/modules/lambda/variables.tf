variable "image_tag" {
  description = "ecr image tag"
  default = "latest"
}

variable "prod_bucket_name" {
  description = "Name of the production model bucket"
  type        = string
}

variable "output_stream_name" {
  description = "Name of the Kinesis output stream"
  type        = string
}

variable "lambda_role_arn" {
  description = "ARN of the IAM role for Lambda"
  type        = string
}

variable "image_uri" {
  description = "URI of the ECR image"
  type        = string
}

variable "input_stream_arn" {
  description = "ARN of the input Kinesis stream"
  type        = string
}
