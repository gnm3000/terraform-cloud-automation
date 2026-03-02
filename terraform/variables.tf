variable "vpc_id" {
  description = "Default VPC ID in us-east-1"
  type        = string
  default     = "vpc-0ec9c9ade2ac85541"
}

variable "project_name" {
  description = "Project name used for AWS resource tagging"
  type        = string
  default     = "cloud-automation"
}

variable "cidr_block" {
  description = "CIDR block allowed for inbound HTTP traffic"
  type        = string
  default     = "0.0.0.0/0"
}

variable "public_subnet_ids" {
  description = "Two public subnet IDs in the default VPC (us-east-1)"
  type        = list(string)
  default = [
    "subnet-0c7804331eac35006",
    "subnet-0e438cdf420995fb2",
  ]
}
