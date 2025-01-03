resource "aws_ssm_parameter" "model_bucket" {
  name  = "/project/model-bucket"
  type  = "String"
  value = var.model_bucket_name
}

resource "aws_ssm_parameter" "predictions_stream_name" {
  name  = "/project/predictions_stream_name"
  type  = "String"
  value = var.output_stream_name
}

