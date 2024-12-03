variable "bucket_name" {
  type = string
  description = "Name of the S3 bucket"
}

variable "AWS_DEFAULT_REGION" {
  type = string
  default = "us-east-1"
}