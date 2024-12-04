variable "mlflow_bucket_arn" {
  description = "ARN of the S3 bucket containing the models"
  type        = string
}

variable "prod_model_bucket_arn" {
  description = "ARN of the production model bucket"
  type        = string
}

variable "input_stream_arn" {
  description = "ARN of the input Kinesis stream"
  type        = string
}

variable "output_stream_arn" {
  description = "ARN of the output Kinesis stream"
  type        = string
}

variable "ecr_repository_arn" {
  description = "ARN of the ECR repository"
  type        = string
}
