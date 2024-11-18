resource "aws_lambda_function" "kinesis_lambda" {
  function_name = var.function_name
  role = aws_iam_role.iam_lambda.arn
  package_type = "Image"
  image_uri = var.image_uri

  tracing_config {
    mode = "Active"
  }

  #optional environment
  environment {
    variables = {
      MODEL_BUCKET = var.model_bucket
      PREDICTIONS_STREAM = var.output_stream_name
    }
  }

  timeout = 100
}

resource "aws_lambda_event_source_mapping" "kinesis_mapping" {
  event_source_arn = var.source_stream_arn
  function_name = aws_lambda_function.kinesis_lambda.arn
  starting_position = "LATEST"
  depends_on = [ aws_iam_role_policy_attachment.kinesis_processing ]

}

resource "aws_lambda_function_event_invoke_config" "kinesis_lambda_event" {
  function_name = aws_lambda_function.kinesis_lambda.arn
  maximum_event_age_in_seconds = 60
  maximum_retry_attempts = 0
}
