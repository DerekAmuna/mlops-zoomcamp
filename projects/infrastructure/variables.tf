variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "prod_bucket_name" {
  description = "Name of the S3 bucket for production model"
  type        = string
}

variable "kinesis_input_stream_name" {
  description = "Name of the Kinesis input stream"
  type        = string
}

variable "kinesis_output_stream_name" {
  description = "Name of the Kinesis output stream"
  type        = string
}

variable "kinesis_shard_count" {
  description = "Number of shards for the Kinesis stream"
  type        = number
  default     = 1
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
}
