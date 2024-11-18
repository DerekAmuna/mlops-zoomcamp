variable "function_name" {
  type = string
}

variable "model_bucket" {
  type = string
}

variable "output_stream_name" {
  type = string
}

variable "source_stream_name" {
  type = string
}

variable "source_stream_arn" {
  type        = string
  description = "Source Kinesis Data Streams stream name"
}

variable "output_stream_arn" {
  description = "ARN of output stream where all the events will be passed"
}

variable "project_id" {
  type = string
  default = "mlops-zoomcamp"
}

variable "image_uri" {
  type = string
}
