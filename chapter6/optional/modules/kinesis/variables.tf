variable "name" {
  type = string
  default = "mlops-zoomcamp"
}

variable "shard_count" {
  type = number
  default = 1
}

variable "retention_period" {
  type = number
  default = 1
}

variable "shard_level_metrics" {
  type = list(string)
  default = [
    "IncomingBytes",
    "OutgoingBytes",
    "IncomingRecords",
    "OutgoingRecords",
    "WriteProvisionedThroughputExceeded",
    "ReadProvisionedThroughputExceeded",
    "IteratorAgeMilliseconds"
  ]
}

variable "tags" {
  type = string
  description = "Tags to set on the Kinesis stream"
  default = "mlops-zoomcamp"
}
