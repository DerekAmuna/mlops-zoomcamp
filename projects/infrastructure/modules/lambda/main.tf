resource "aws_lambda_function" "wine_quality_predictor" {
  function_name    = "wine_quality_predictor"
  role            = var.lambda_role_arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  package_type    = "Image"
  image_uri       = var.image_uri

  environment {
    variables = {
      MODEL_BUCKET = var.prod_bucket_name
      PREDICTIONS_STREAM = var.output_stream_name
    }
  }
}

resource "aws_lambda_event_source_mapping" "kinesis_trigger" {
  event_source_arn  = var.input_stream_arn
  function_name     = aws_lambda_function.wine_quality_predictor.function_name
  starting_position = "LATEST"
  batch_size        = 1
  enabled           = true
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function_event_invoke_config" "kinesis_lambda_event" {
  function_name = aws_lambda_function.wine_quality_predictor.arn
  maximum_event_age_in_seconds = 60
  maximum_retry_attempts = 0
}