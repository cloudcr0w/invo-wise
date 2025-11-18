variable "project_name" {
  type        = string
  description = "Base name for InvoWise resources (used in bucket/table names, tags etc.)"
  default     = "invo-wise"
}

variable "environment" {
  type        = string
  description = "Deployment environment (e.g. dev, stage, prod)"
  default     = "dev"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources into"
  default     = "eu-central-1"
}

variable "enable_backend" {
  type        = bool
  description = "Whether to actually create S3/DynamoDB backend resources when count-guards are added"
  default     = false
}

variable "common_tags" {
  type = map(string)
  description = "Base tags applied to all InvoWise infrastructure resources"

  default = {
    Project     = "InvoWise"
    ManagedBy   = "Terraform"
    Environment = "dev"
  }
}
