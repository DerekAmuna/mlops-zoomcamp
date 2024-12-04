resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
}


output "prod_model_bucket_name" {
  description = "Name of the production model bucket"
  value       = aws_s3_bucket.s3_bucket.id
}

output "prod_model_bucket_arn" {
  description = "ARN of the production model bucket"
  value       = aws_s3_bucket.s3_bucket.arn
}

output "mlflow_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.s3_bucket.id
}

output "mlflow_bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.s3_bucket.arn
} 