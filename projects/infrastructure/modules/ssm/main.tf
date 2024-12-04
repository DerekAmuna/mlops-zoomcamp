resource "aws_ssm_parameter" "mlflow_run_id" {
  name  = "/wine-quality/mlflow-run-id"
  type  = "String"
  value = var.mlflow_run_id
}

resource "aws_ssm_parameter" "model_bucket" {
  name  = "/wine-quality/model-bucket"
  type  = "String"
  value = var.model_bucket_name
}

resource "aws_ssm_parameter" "experiment_id" {
  name  = "/wine-quality/experiment-id"
  type  = "String"
  value = var.experiment_id
} 