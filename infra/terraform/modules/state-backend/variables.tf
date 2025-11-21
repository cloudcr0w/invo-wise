variable "project_name" {
  type        = string
  description = "Base name for state backend resources (S3/DynamoDB)."
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev/stage/prod)."
}

variable "tags" {
  type        = map(string)
  description = "Common tags applied to all state backend resources."
}
