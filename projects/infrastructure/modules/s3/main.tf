resource "aws_s3_bucket" "mlflow_bucket" {
  bucket = var.bucket_name
}
