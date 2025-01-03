data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_lambda_function" "kinesis_lambda" {
  depends_on = [ var.ecr_image_resource ]
  function_name = var.lambda_function_name
  role = aws_iam_role.iam_lambda.arn
  package_type = "Image"
  image_uri = var.image_uri
  architectures = ["x86_64"]

  tracing_config {
    mode = "Active"
  }

  #optional environment
  environment {
    variables = {
      MODEL_BUCKET = var.model_bucket
      PREDICTIONS_STREAM_NAME = var.output_stream_name
    }
  }

  timeout = 300
  memory_size = 1024
}

resource "aws_lambda_event_source_mapping" "kinesis_mapping" {
  event_source_arn = var.source_stream_arn
  function_name = aws_lambda_function.kinesis_lambda.arn
  starting_position = "LATEST"
  depends_on = [ aws_iam_role_policy_attachment.kinesis_processing ]

  enabled           = true
  batch_size        = 1

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function_event_invoke_config" "kinesis_lambda_event" {
  function_name = aws_lambda_function.kinesis_lambda.arn
  maximum_event_age_in_seconds = 60
  maximum_retry_attempts = 0
}

# Create SSM policy
resource "aws_iam_policy" "ssm_policy" {
  name = "ssm_policy_${var.lambda_function_name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = [
          "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/project/*"
        ]
      }
    ]
  })
}

# Attach SSM policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_ssm" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.ssm_policy.arn
}