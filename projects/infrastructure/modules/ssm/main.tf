resource "aws_ssm_parameter" "model_bucket" {
  name  = "/project/model-bucket"
  type  = "String"
  value = module.s3_bucket.name
}

resource "aws_ssm_parameter" "predictions_stream" {
  name  = "/project/predictions-stream"
  type  = "String"
  value = module.output_wine_stream.stream_name
}
