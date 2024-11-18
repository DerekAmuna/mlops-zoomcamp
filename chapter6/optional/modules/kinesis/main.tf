resource "aws_kinesis_stream" "ride_stream" {
  name = var.name
  shard_count = var.shard_count
  retention_period = var.retention_period
  shard_level_metrics = var.shard_level_metrics
  tags = {
    CreatedBy = var.tags
  }
}

output "stream_arn" {
  value = aws_kinesis_stream.ride_stream.arn
}
