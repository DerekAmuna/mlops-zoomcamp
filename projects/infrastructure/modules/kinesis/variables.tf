variable "kinesis_stream_name" {
  description = "Name of the Kinesis input stream"
  type        = string
}

variable "kinesis_shard_count" {
  description = "Number of input shards"
  type        = number
}
