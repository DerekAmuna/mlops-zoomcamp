output "bucket_name" {
  description = "Name of the created S3 bucket"
  value       = module.mlflow_s3.bucket_name
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = module.mlflow_s3.bucket_arn
} 