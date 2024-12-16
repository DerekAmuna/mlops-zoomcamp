variable "mlflow_run_id" {
  description = "ID of the mlflow run"
  type        = string
}

variable "model_bucket_name" {
  description = "Name of the S3 bucket for model"
  type        = string
}

variable "experiment_id" {
  description = "ID of the mlflow experiment"
  type        = string
}