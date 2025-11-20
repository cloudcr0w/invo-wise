###############################################################################
# Providers & Terraform configuration
###############################################################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend (S3) will be configured later in Phase 5.
  # backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  # Credentials are expected via standard AWS mechanisms:
  # - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_PROFILE)
  # - Shared credentials file (~/.aws/credentials)
  # - IAM role (when running in AWS)
}
